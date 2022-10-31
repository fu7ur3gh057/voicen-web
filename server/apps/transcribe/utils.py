import os
from decimal import Decimal
import unicodedata
import string

from server import settings

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 250


def transcribe_file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'transcribe/user_{0}/{1}'.format(instance.profile.user.id, filename)


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


def transcribe_ftp_path(user_id, file_id, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    filename = clean_filename(filename)
    return f'transcribe/user_{user_id}/{file_id}__{filename}'


def get_filename(text):
    if len(text) > 40:
        return f'{text[:39]}'
    else:
        return f'{text}'


def get_filepath(filename, user_id):
    return f"media/stt/user_{user_id}/{filename}"


def get_transcribe_price(duration: float):
    stt_price = 0.06
    price = round((Decimal((duration) * int(stt_price) / 60)), 5)
    print('PRICE IS', price)
    return price


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


def delete_file(file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)
