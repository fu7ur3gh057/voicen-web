from celery import shared_task
from celery.utils.log import get_task_logger

from storage.ftp import FTPStorage

logger = get_task_logger(__name__)


# SAVE SYNTHESIS TEXT
# @shared_task(name='save_synthesis_text')
# def save_synthesis_text(data):
#     ftp_storage = FTPStorage()
#     pass
#
#
# # SAVE SYNTHESIS FILE
# @shared_task(name='save_synthesis_file')
# def save_synthesis_file(data):
#     ftp_storage = FTPStorage()
#     pass


# DELETE SYNTHESIS
@shared_task(name='delete_synthesis')
def delete_synthesis_task(data):
    ftp_path = data['ftp_path']
    # Delete file from FTP server
    ftp_storage = FTPStorage()
    ftp_storage.delete(name=ftp_path)
    return 'Transcribe job was deleted successfuly'
