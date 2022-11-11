import logging
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import Q
from apps.payment.api.serializers import OperationSerializer, WalletSerializer, TransactionSerializer, \
    SubscriptionSerializer
from apps.payment.models import Operation, Subscription, Transaction
from apps.payment.pagination import TransactionPagination, OperationPagination, SubscriptionPagination
from apps.payment.renderers import WalletJSONRenderer
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)


# ALL METHODS ARE AUTHENTICATED

# GET WALLET BY USER
class GetWalletAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [WalletJSONRenderer]
    serializer_class = WalletSerializer

    def get(self, request: Request):
        user = self.request.user
        profile = user.profile
        wallet = profile.wallet
        serializer = self.serializer_class(wallet)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# MAKE TRANSACTION
class MakeTransactionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request):
        wallet = request.user.profile.wallet
        amount = Decimal(request.data['amount'])
        if amount > 1:
            wallet.credit += amount
            transaction = Transaction.objects.create(wallet=wallet, amount=amount, type=1)
            transaction.save()
            wallet.save()
            return Response({"success": f'Current user balance is {wallet.credit}'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Amount should be more than 1$"}, status=status.HTTP_402_PAYMENT_REQUIRED)


# GET LIST OF TRANSACTIONS
class TransactionListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination
    queryset = Transaction.objects.all()

    def get_queryset(self):
        wallet = self.request.user.profile.wallet
        queryset = self.queryset.filter(wallet=wallet).order_by('-created_at')
        return queryset


# GET LIST OF OPERATIONS
class OperationListAPIView(generics.ListAPIView):
    queryset = Operation.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OperationSerializer
    pagination_class = OperationPagination

    def get_queryset(self):
        wallet = self.request.user.profile.wallet
        queryset = self.queryset.filter(wallet=wallet).order_by('-created_at')
        return queryset


# GET LIST OF SUBSCRIPTION
class SubscriptionListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionSerializer
    pagination_class = SubscriptionPagination
    queryset = Subscription.objects.all()

    def get_queryset(self):
        wallet = self.request.user.profile.wallet
        queryset = self.queryset.filter(Q(wallet=wallet) & ~Q(type=4)).order_by('-created_at')
        return queryset


# MAKE SUBSCRIPTION
class SubscribeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request):
        wallet = request.user.profile.wallet
        if wallet.credit < 15:
            return Response("Not enough credits", status=status.HTTP_402_PAYMENT_REQUIRED)
        subscription_list = Subscription.objects.all().filter(wallet=wallet)
        active_subscriptions = subscription_list.filter(type=1)
        if len(active_subscriptions) != 0:
            return Response("Subscription is already Active", status=status.HTTP_200_OK)
        subscription = Subscription.objects.create(wallet=wallet, type=1)
        subscription.save()
        wallet.credit -= 15
        wallet.save()
        return Response("Subscription is Active", status=status.HTTP_201_CREATED)


# MAKE UNSUBSCRIBE
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def unsubscribe(request: Request):
    wallet = request.user.profile.wallet
    active_subscriptions = Subscription.objects.all().filter(wallet=wallet).filter(type=1)
    if len(active_subscriptions) > 0:
        return Response("Subscription is Canceled", status=status.HTTP_200_OK)
    else:
        return Response("There aren't active subscription", status=status.HTTP_204_NO_CONTENT)
