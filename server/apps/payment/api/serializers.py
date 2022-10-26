from rest_framework import serializers

from apps.payment.models import Operation, Subscription, Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="profile.user.email", read_only=True)
    username = serializers.CharField(source="profile.user.username", read_only=True)

    class Meta:
        model = Wallet
        fields = ["email", "username", "credit"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "type",
            "created_at",
        ]


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = [
            "id",
            "amount",
            "type",
            "created_at",
        ]


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['__all__']


# class CreateSubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
