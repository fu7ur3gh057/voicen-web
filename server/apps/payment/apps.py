from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.payment'

    def ready(self):
        pass
        # from apps.payment import signals
        # from .models import SubscriptionChecker
        # if SubscriptionChecker.objects.all().count() == 0:
        #     checker = SubscriptionChecker.objects.create(title='First')
        #     checker.save()
