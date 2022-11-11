import os
from decimal import Decimal
import unicodedata
import string
from urllib.parse import urlparse

from server import settings

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 250


# FILE PATH FOR MEDIA ROOT
def transcribe_file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'transcribe/user_{0}/{1}'.format(instance.profile.user.id, filename)


# DELETE FILE FROM MEDIA ROOT
def delete_file(file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)


# CLEAN FILENAME FOR FTP SERVER
def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    filename, extension = os.path.splitext(filename)
    for r in replace:
        filename = filename.replace(r, '_')
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize(
        'NFKD', filename).encode('ASCII', 'ignore').decode()
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    return cleaned_filename[:char_limit] + extension


# FILE PATH FOR FTP SERVER
def transcribe_ftp_path(user_id, file_id, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    filename = clean_filename(filename)
    return f'transcribe/user_{user_id}/{file_id}__{filename}'


# GET SHORT NAME
def get_filename(text):
    if len(text) > 40:
        return f'{text[:39]}'
    else:
        return f'{text}'


# GET TRANSCRIBE PRICE
def get_transcribe_price(duration: float):
    stt_price = 0.06
    price = round((Decimal((duration) * stt_price / 60)), 5)
    return price


# GET YOUTUBE ID FROM URL
def youtube_id(url):
    o = urlparse(url)
    if o.netloc == 'youtu.be':
        return o.path[1:]
    elif o.netloc in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
        if o.path == '/watch':
            id_index = o.query.index('v=')
            return o.query[id_index + 2:id_index + 13]
        elif o.path[:7] == '/embed/':
            return o.path.split('/')[2]
        elif o.path[:3] == '/v/':
            return o.path.split('/')[2]
    elif o.netloc == '':
        id_index = o.query.index('v=')
        return o.query[id_index + 2:id_index + 13]
    return None  # if fail


# GET YOUTUBE API URL
def get_youtube_api_url(yt_id: str, yt_api_key: str):
    base_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = 'fields=items(id,snippet(title),contentDetails(duration))&part=snippet,contentDetails'
    return f'{base_url}?id={yt_id}&key={yt_api_key}&{params}'


# GET TRANSCRIBE STATUS
def get_transcribe_status(status: int):
    if status == -1:
        return "waiting"
    elif status == 0:
        return "preparing"
    elif status == 1:
        return "processing"
    elif status == 2:
        return "synthesizing"
    elif status == 3:
        return "ready"
    elif status == 4:
        return "failed"
    else:
        return "unknown"
