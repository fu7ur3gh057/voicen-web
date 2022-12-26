from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.common'

    def ready(self):
        pass
        # from apps.common.models import VoicenConfiguration
        # if VoicenConfiguration.objects.all().count() == 0:
        #     config = VoicenConfiguration.objects.create()
        #     config.save()
