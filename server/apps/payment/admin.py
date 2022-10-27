from django.contrib import admin

from .models import Operation, Transaction, Subscription, Wallet


class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'pkid', 'profile', "created_at"]
    list_display_links = ['id', 'pkid', "profile"]


class OperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'pkid', 'wallet', 'type', 'amount', "created_at"]
    list_display_links = ['id', 'pkid', "wallet"]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'pkid', 'wallet', 'type', 'amount', "created_at"]
    list_display_links = ['id', 'pkid', "wallet"]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'pkid', 'type']
    list_display_links = ['id', 'pkid']


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
