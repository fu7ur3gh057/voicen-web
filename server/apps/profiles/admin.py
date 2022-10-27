from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "user", "phone_number", "city", "is_trial", "is_subscribed"]
    list_filter = ["city", "is_trial", "is_subscribed"]
    list_display_links = ["id", "pkid", "user", ]


admin.site.register(Profile, ProfileAdmin)
