from celery import shared_task
from celery.utils.log import get_task_logger

import datetime

from apps.payment.models import Subscription

logger = get_task_logger(__name__)


@shared_task(name='subscription_checker')
def subscription_checker_task():
    active_subscriptions = Subscription.objects.all().filter(type=1)
    today = datetime.date.today()
    for sub in active_subscriptions:
        end_time = sub.end_time
        if today.month is end_time.month:
            if today.day >= end_time.day:
                sub.type = 2
                sub.save()
    message = "All Subscriptions are checked"
    logger.info(message)
    return message
