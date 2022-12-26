from django.contrib import admin

from apps.common.models import VoicenConfiguration


class VoicenConfigurationAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at']
    list_display_links = ['id', 'created_at', 'updated_at']


admin.site.register(VoicenConfiguration, VoicenConfigurationAdmin)
