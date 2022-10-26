import logging
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from apps.payment.api.serializers import OperationSerializer, WalletSerializer, TransactionSerializer, \
    SubscriptionSerializer
from apps.payment.models import Operation, Subscription, Transaction
from apps.payment.pagination import TransactionPagination
from apps.payment.renderers import WalletJSONRenderer
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)


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


class TransactionListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination
    queryset = Transaction.objects.all()
    ordering_fields = ['created_at']

    def get_queryset(self):
        wallet = self.request.user.profile.wallet
        queryset = Transaction.objects.filter(wallet=wallet).order_by('-created_at')
        return queryset


class ListOperationAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pass


class SubscribeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        pass

    def post(self, request: Request):
        wallet = request.user.profile.wallet
        if wallet.credit < 15:
            return Response("Not enough credits", status=status.HTTP_402_PAYMENT_REQUIRED)
        if wallet.subscription is None:
            subscription = Subscription.objects.create(type=1)
            subscription.save()
            wallet.subscription = subscription
            wallet.credit -= 15
            wallet.save()
            return Response("Subscription is Active", status=status.HTTP_201_CREATED)
        else:
            if wallet.subscription.type == 2 or wallet.subscription.type == 3:
                subscription = wallet.subscription
                subscription.type = 1
                subscription.save()
                wallet.credit -= 15
                wallet.save()
                return Response("Subscription is Active", status=status.HTTP_200_OK)
            # Subscription is Active
            else:
                return Response("Subscription is already active", status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def unsubscribe(request: Request):
    pass
