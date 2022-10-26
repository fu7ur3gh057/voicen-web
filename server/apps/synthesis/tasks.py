from celery import shared_task
from celery.utils.log import get_task_logger
import random
import time

logger = get_task_logger(__name__)


@shared_task(name='delete_synthesis')
def delete_synthesis_task(file_path):
    pass
