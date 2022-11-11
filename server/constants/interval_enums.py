from enum import Enum
from django_celery_beat.models import IntervalSchedule


class TimeInterval(Enum):
    five_sec = '5 seconds'
    half_min = '30 seconds'
    one_min = '1 minute'
    three_min = '3 minutes'
    five_min = '5 minutes'
    ten_min = '10 minutes'
    half_hour = '30 minutes'
    one_hour = '1 hour'
    half_day = '6 hours'
    one_day = '1 days'
    fifteen_day = '15 days'


class TaskStatus(Enum):
    active = 'Active'
    disabled = 'Disabled'


def interval_schedule(self, time_interval):
    if time_interval == TimeInterval.five_sec:
        return IntervalSchedule.objects.get(every=5, period='seconds')
    if time_interval == TimeInterval.half_min:
        return IntervalSchedule.objects.get(every=30, period='seconds')
    if time_interval == TimeInterval.one_min:
        return IntervalSchedule.objects.get(every=1, period='minutes')
    if time_interval == TimeInterval.three_min:
        return IntervalSchedule.objects.get(every=3, period='minutes')
    if time_interval == TimeInterval.five_min:
        return IntervalSchedule.objects.get(every=5, period='minutes')
    if time_interval == TimeInterval.ten_min:
        return IntervalSchedule.objects.get(every=10, period='minutes')
    if time_interval == TimeInterval.half_hour:
        return IntervalSchedule.objects.get(every=30, period='minutes')
    if time_interval == TimeInterval.one_hour:
        return IntervalSchedule.objects.get(every=1, period='hours')
    if time_interval == TimeInterval.half_day:
        return IntervalSchedule.objects.get(every=12, period='hours')
    if time_interval == TimeInterval.one_day:
        return IntervalSchedule.objects.get(every=1, period='day')
    if time_interval == TimeInterval.fifteen_day:
        return IntervalSchedule.objects.get(every=15, period='day')
    raise NotImplementedError
