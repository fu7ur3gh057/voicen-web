from django.contrib import admin

from apps.chat.models import Room, Message


# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    list_filter = ["user"]
    list_display_links = ["id", "user"]


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'pkid', 'user', 'created_at', 'get_text']
    list_filter = ["user"]
    list_display_links = ["id", 'pkid', "user"]

    def get_text(self, obj):
        if len(obj.text) > 30:
            return f'{obj.text[0:28]}...'
        else:
            return obj.text


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
