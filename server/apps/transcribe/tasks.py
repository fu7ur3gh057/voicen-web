from celery import shared_task
from celery.utils.log import get_task_logger

from apps.transcribe.models import Transcribe
from apps.transcribe.utils import transcribe_ftp_path, clean_filename, delete_file
from storage.ftp import FTPStorage

logger = get_task_logger(__name__)


# SAVE TRANSCRIBE FILE
@shared_task(name='save_transcribe_file')
def save_transcribe_file(data):
    transcribe_id = data['transcribe_id']
    # Get transcribe
    transcribe = Transcribe.objects.get(id=transcribe_id)
    file_path = str(transcribe.file)
    user = transcribe.profile.user
    ftp_path = transcribe_ftp_path(user_id=user.id, file_id=transcribe.id, filename=transcribe.file_name[0:100])
    # Save file to FTP server
    ftp_storage = FTPStorage()
    ftp_storage._save(ftp_path, transcribe.file)
    # Deleting temp file from Media Root
    delete_file(file_path=file_path)
    transcribe.ftp_path = ftp_path
    transcribe.file = None
    transcribe.save()
    return f'User {user.email} saved transcribe Job to FTP Storage ::: {file_path}'


# SAVE TRANSCRIBE YOUTUBE
@shared_task(name='save_transcribe_youtube')
def save_transcribe_youtube(data):
    pass


# DELETE TRANSCRIBE
@shared_task(name='delete_transcribe')
def delete_transcribe(data):
    ftp_path = data['ftp_path']
    # Delete file from FTP server
    ftp_storage = FTPStorage()
    ftp_storage.delete(name=ftp_path)
    return 'Transcribe job was deleted successfuly'
