from django.contrib import admin

from apps.synthesis.models import Synthesis


class SynthesisAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'char_count', 'lang', 'status', 'created_at']
    list_filter = ['profile', 'lang', 'status']
    list_display_links = ['id', 'profile', 'char_count', 'lang']


admin.site.register(Synthesis, SynthesisAdmin)
