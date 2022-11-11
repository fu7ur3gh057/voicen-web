import os.path
import io
from datetime import datetime

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import ftplib
import ssl
from urllib.parse import urlparse
from django.core.files.base import File


class FTPStorageException(Exception):
    pass


# BASE FTP STORAGE
@deconstructible
class FTPStorage(Storage):
    def __init__(self, location=None, base_url=None):
        location = location or settings.FTP_STORAGE_LOCATION
        if location is None:
            raise ImproperlyConfigured("You must set a location at "
                                       "instanciation or at "
                                       " settings.FTP_STORAGE_LOCATION'.")
        self.location = location
        base_url = base_url or settings.MEDIA_URL
        self._config = self._decode_location(location)
        self._base_url = base_url
        self._connection = None

    # DECODING LOCATION URL
    def _decode_location(self, location):
        splitted_url = urlparse(location)
        config = {}
        if splitted_url.scheme not in ('ftp', 'aftp'):
            raise ImproperlyConfigured('FTPStorage works only with FTP protocol!')
        if splitted_url.hostname == '':
            raise ImproperlyConfigured('You must at least provide hostname!')
        if splitted_url.scheme == 'aftp':
            config['active'] = True
        else:
            config['active'] = False
        config['path'] = splitted_url.path
        config['host'] = splitted_url.hostname
        config['user'] = splitted_url.username
        config['passwd'] = splitted_url.password
        config['port'] = int(splitted_url.port or "21")
        return config

    # CONNECT
    def _start_connection(self):
        # Check if connection is still alive and if not, drop it.
        if self._connection is not None:
            try:
                self._connection.pwd()
            except ftplib.all_errors:
                self._connection = None
        # Real reconnect
        if self._connection is None:
            try:
                host = self._config['host']
                user = self._config['user']
                passwd = self._config['passwd']
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.load_verify_locations(settings.PATH_TO_CA_CERT_CHAIN)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_REQUIRED
                ftp = ftplib.FTP_TLS(host=host, user=user, passwd=passwd, context=context)
                ftp.prot_p()
                l = ftp.nlst()
                self._connection = ftp
                return
            except ftplib.all_errors:
                raise FTPStorageException(
                    'Connection or login error using data %s'
                    % repr(self._config)
                )

    # DISCONNECT
    def _disconnect(self):
        self._connection.quit()
        self._connection = None

    # MAKE DIRECTORY
    def _mkremdirs(self, path):
        pwd = self._connection.pwd()
        self._connection.cwd('fuad')
        path_splitted = path.split('/')
        for path_part in path_splitted:
            try:
                self._connection.cwd(f'{path_part}')
            except ftplib.all_errors:
                try:
                    self._connection.mkd(path_part)
                    self._connection.cwd(path_part)
                except ftplib.all_errors:
                    raise FTPStorageException(
                        'Cannot create directory chain %s' % path
                    )
        self._connection.cwd(pwd)
        return

    # PUT FILE
    def _put_file(self, name, content):
        name = f'fuad/{name}'
        try:
            self._mkremdirs(os.path.dirname(name))
            pwd = self._connection.pwd()
            f_s = os.path.dirname(name)
            self._connection.cwd(os.path.dirname(name))
            self._connection.storbinary(f'STOR {os.path.basename(name)}', content.file, content.DEFAULT_CHUNK_SIZE)
            self._connection.cwd(pwd)
        except ftplib.all_errors:
            raise FTPStorageException('Error writing file %s' % name)

    def _open(self, name, mode='rb'):
        remote_file = FTPStorageFile(name, self, mode=mode)
        return remote_file

    def _read(self, name):
        memory_file = io.BytesIO()
        try:
            pwd = self._connection.pwd()
            self._connection.cwd(os.path.dirname(name))
            self._connection.retrbinary('RETR ' + os.path.basename(name),
                                        memory_file.write)
            self._connection.cwd(pwd)
            memory_file.seek(0)
            return memory_file
        except ftplib.all_errors:
            raise FTPStorageException('Error reading file %s' % name)

    def _save(self, name, content):
        content.open()
        self._start_connection()
        self._put_file(name, content)
        content.close()
        return name

    def size(self, name):
        self._start_connection()
        try:
            dirs, files = self._get_dir_details(os.path.dirname(name))
            if os.path.basename(name) in files:
                return files[os.path.basename(name)]
            else:
                return 0
        except FTPStorageException:
            return 0

    def file_size(self, path):
        self._start_connection()
        return self._connection.size(path)

    def _get_dir_details(self, path):
        # Connection must be open!
        try:
            lines = []
            self._connection.retrlines('LIST ' + path, lines.append)
            dirs = {}
            files = {}
            for line in lines:
                words = line.split()
                if len(words) < 6:
                    continue
                if words[-2] == '->':
                    continue
                if words[0][0] == 'd':
                    dirs[words[-1]] = 0
                elif words[0][0] == '-':
                    files[words[-1]] = int(words[-5])
            return dirs, files
        except ftplib.all_errors:
            raise FTPStorageException('Error getting listing for %s' % path)

    def modified_time(self, name):
        self._start_connection()
        resp = self._connection.sendcmd('MDTM ' + name)
        if resp[:3] == '213':
            s = resp[3:].strip()
            # workaround for broken FTP servers returning responses
            # starting with e.g. 1904... instead of 2004...
            if len(s) == 15 and s[:2] == '19':
                s = str(1900 + int(s[2:5])) + s[5:]
            return datetime.strptime(s, '%Y%m%d%H%M%S')
        raise FTPStorageException(
            'Error getting modification time of file %s' % name
        )

    def listdir(self, path):
        self._start_connection()
        try:
            dirs, files = self._get_dir_details(path)
            return list(dirs.keys()), list(files.keys())
        except FTPStorageException:
            raise

    def delete(self, name):
        name = f'fuad/{name}'
        if not self.exists(name):
            return
        self._start_connection()
        try:
            self._connection.delete(name)
        except ftplib.all_errors:
            raise FTPStorageException('Error when removing %s' % name)

    def exists(self, name):
        self._start_connection()
        try:
            nlst = self._connection.nlst(
                os.path.dirname(name) + '/'
            )
            if name in nlst or os.path.basename(name) in nlst:
                return True
            else:
                return False
        except ftplib.error_temp:
            return False
        except ftplib.error_perm:
            # error_perm: 550 Can't find file
            return False
        except ftplib.all_errors:
            raise FTPStorageException(
                'Error when testing existence of %s' % name)

    def url(self, name):
        if self._base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return urlparse.urljoin(self._base_url, name).replace('\\', '/')


class FTPStorageFile(File):
    def __init__(self, name, storage, mode):
        self.name = name
        self._storage = storage
        self._mode = mode
        self._is_dirty = False
        self.file = io.BytesIO()
        self._is_read = False

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self.name)
        return self._size

    def readlines(self):
        if not self._is_read:
            self._storage._start_connection()
            self.file = self._storage._read(self.name)
            self._is_read = True
        return self.file.readlines()

    def read(self, num_bytes=None):
        if not self._is_read:
            self._storage._start_connection()
            self.file = self._storage._read(self.name)
            self._is_read = True
        return self.file.read(num_bytes)

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was opened for read-only access.")
        self.file = io.BytesIO(content)
        self._is_dirty = True
        self._is_read = True

    def close(self):
        if self._is_dirty:
            self._storage._start_connection()
            self._storage._put_file(self.name, self)
            self._storage.disconnect()
        self.file.close()
