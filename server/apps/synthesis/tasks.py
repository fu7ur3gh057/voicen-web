from celery import shared_task
from celery.utils.log import get_task_logger

from storage.ftp import FTPStorage

logger = get_task_logger(__name__)


@shared_task(name='save_synthesis')
def save_synthesis_task(data):
    ftp_storage = FTPStorage()
    pass


@shared_task(name='delete_synthesis')
def delete_synthesis_task(file_path):
    pass
