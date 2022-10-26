from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
import random
import time

logger = get_task_logger(__name__)


@shared_task(name='activate_user')
def activate_user(data):
    logger.info('EMAIL START TO SEND')
    is_task_completed = False
    try:
        is_task_completed = True
    except Exception as ex:
        logger.error(str(ex))
    if is_task_completed:
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['receivers']])
        email.send()
    print('email has sent')
    return f'Email has send to {data["receivers"]}'