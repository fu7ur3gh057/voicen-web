from django.contrib import admin

from apps.transcribe.models import Transcribe


# Register your models here.
class TranscribeAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'profile', 'lang', 'duration', 'status', 'created_at']
    list_filter = ['profile', 'lang', 'status']
    list_display_links = ['file_name', 'profile', 'duration', 'lang']


admin.site.register(Transcribe, TranscribeAdmin)
