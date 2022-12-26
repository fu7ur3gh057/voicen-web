from django.contrib import admin

from .models import Operation, Transaction, Subscription, Wallet, SubscriptionChecker, EPointLogs


class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'pkid', 'profile', 'credit', "created_at"]
    list_filter = ['profile']
    list_display_links = ['id', 'pkid', "credit", "profile"]


class OperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'pkid', 'wallet', 'type', 'amount', "created_at"]
    list_filter = ['wallet', 'type']
    list_display_links = ['id', 'pkid', "wallet"]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'pkid', 'wallet', 'type', 'amount', "created_at"]
    list_filter = ['wallet', 'type']
    list_display_links = ['id', 'pkid', "wallet"]


class EPointLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'wallet', "created_at"]
    list_filter = ['wallet']
    list_display_links = ['id', "wallet"]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'pkid', 'wallet', 'type', "created_at"]
    list_filter = ['wallet', 'type']
    list_display_links = ['id', 'pkid', 'wallet', "created_at"]


class SubscriptionCheckerAdmin(admin.ModelAdmin):
    list_display = ['title', 'time_interval', 'status']
    list_display_links = ['title', 'time_interval', 'status']


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(EPointLogs, EPointLogsAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionChecker, SubscriptionCheckerAdmin)
