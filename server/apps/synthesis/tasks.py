from celery import shared_task
from celery.utils.log import get_task_logger
from django.shortcuts import get_object_or_404

from apps.synthesis.models import Synthesis
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
    job_id_list = data['id_list']
    ftp_storage = FTPStorage()
    for job_id in job_id_list:
        synthesis = get_object_or_404(Synthesis, id=job_id)
        if synthesis is not None:
            ftp_path = synthesis.ftp_path
            # Delete object from Database
            synthesis.delete()
            # Delete file from FTP server
            ftp_storage.delete(name=ftp_path)
    return 'Synthesis jobs was deleted successfuly'
