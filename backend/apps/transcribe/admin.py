from django.contrib import admin

from apps.transcribe.models import Transcribe


# Register your models here.
class TranscribeAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'lang', 'duration', 'status', 'created']
    list_filter = ['profile', 'lang', 'status']
    list_display_links = ['id', 'profile', 'duration', 'lang']
    # formfield_overrides = {
    #     models.JSONField: {'widget': JSONEditor},
    # }


admin.site.register(Transcribe, TranscribeAdmin)
