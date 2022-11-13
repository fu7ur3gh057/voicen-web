from celery import shared_task
from celery.utils.log import get_task_logger
from pathlib import Path
from apps.transcribe.models import Transcribe
from apps.transcribe.utils import transcribe_ftp_path, clean_filename, delete_file, download_yt_video_as_mp3
from storage.ftp import FTPStorage

logger = get_task_logger(__name__)


# SAVE TRANSCRIBE FILE
@shared_task(name='save_transcribe_file')
def save_transcribe_file_task(data):
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
def save_transcribe_youtube_task(data):
    transcribe_id = data['transcribe_id']
    video_info = data['video_info']
    transcribe = Transcribe.objects.get(id=transcribe_id)
    user = transcribe.profile.user
    try:
        # Saving Youtube video to Media Root as MP3
        file_path = download_yt_video_as_mp3(video_info=video_info, user_id=user.id)
        transcribe.file = file_path
        ftp_path = transcribe_ftp_path(user_id=user.id, file_id=transcribe.id, filename=transcribe.file_name[0:100])
        # Save file to FTP server
        ftp_storage = FTPStorage()
        ftp_storage._save(name=ftp_path, content=file_path, is_file=False)
        # Deleting temp file from Media Root
        delete_file(file_path=file_path)
        transcribe.ftp_path = ftp_path
        transcribe.file = None
        transcribe.save()
        return f'User {user.email} saved transcribe Job to FTP Storage ::: {file_path}'
    except Exception as ex:
        print(ex)


# DELETE TRANSCRIBE
@shared_task(name='delete_transcribe')
def delete_transcribe_task(data):
    ftp_path = data['ftp_path']
    # Delete file from FTP server
    ftp_storage = FTPStorage()
    ftp_storage.delete(name=ftp_path)
    return 'Transcribe job was deleted successfuly'
