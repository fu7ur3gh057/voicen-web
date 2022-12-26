import logging
import base64
import hashlib
import json
import urllib.parse

from decimal import Decimal

import requests
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import Q
from apps.payment.api.serializers import OperationSerializer, WalletSerializer, TransactionSerializer, \
    SubscriptionSerializer
from apps.payment.models import Operation, Subscription, Transaction, EPointLogs, Wallet
from apps.payment.pagination import TransactionPagination, OperationPagination, SubscriptionPagination
from apps.payment.renderers import WalletJSONRenderer
from apps.profiles.models import Profile
from server import settings

logger = logging.getLogger(__name__)


# ALL METHODS ARE AUTHENTICATED

# GET WALLET BY USER
class GetWalletAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
        amount = round(Decimal(request.data['amount']), 2)
        public_key = settings.EPOINT_PUBLIC_KEY
        private_key = settings.EPOINT_PRIVATE_KEY
        if amount < 1:
            return Response({"error": "Amount should be more than 1$"}, status=status.HTTP_402_PAYMENT_REQUIRED)
        elif amount > 10000:
            return Response({"error": "Amount should be less than 10 000$"}, status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            dollar_difference = Decimal(1.7)
            amount = round(Decimal(amount * dollar_difference), 2)
            wallet.credit += amount
            # create json string
            json_data = {
                'public_key': public_key,
                'amount': str(amount),
                'currency': "AZN",
                'description': f"Voicen Payment - {request.user.first_name} {request.user.last_name} ({request.user.email})",
                'order_id': str(wallet.id),
                'language': 'en'
            }
            data = base64.b64encode(json.dumps(json_data).encode()).decode()
            sgn_string = private_key + data + private_key
            digest = hashlib.sha1(sgn_string.encode()).digest()
            signature = base64.b64encode(digest).decode()
            # create request
            request_data = urllib.parse.urlencode({'data': data, 'signature': signature})
            # send request
            response = requests.post(
                'https://epoint.az/api/1/request',
                data=request_data,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            )
            # get response
            response_data = response.json()
            if response.status_code == 200 and response_data.get('status') == 'success':
                redirect_url = urllib.parse.unquote(response_data.get('redirect_url'))
                EPointLogs.objects.create(
                    wallet=wallet,
                    request_body=request_data,
                    response_body=json.dumps(request_data)
                )
                return Response(f'{redirect_url}', status=status.HTTP_200_OK)
            else:
                return Response(f'Error', status=status.HTTP_402_PAYMENT_REQUIRED)


class ReceiveTransactionAPIView(APIView):
    serializer_class = TransactionSerializer

    def post(self, request):
        try:
            request_body = request.POST.copy()
            if not request_body.get('data'):
                return Response('No data', status=status.HTTP_400_BAD_REQUEST)
            private_key = settings.EPOINT_PRIVATE_KEY
            epoint_signature = request_body.get('signature')
            sgn_string = private_key + request_body.get('data') + private_key
            digest = hashlib.sha1(sgn_string.encode()).digest()
            signature = base64.b64encode(digest).decode()
            if epoint_signature != signature:
                return Response('Signature does not match.', status=status.HTTP_400_BAD_REQUEST)
            data = json.loads(base64.b64decode(request_body.get('data')).decode())
            if data.get('status') == 'success':
                wallet = Wallet.objects.get(id=data['order_id'])
                amount = round(Decimal(request.data['amount']), 2)
                wallet.credit += amount
                profile = wallet.profile
                profile.is_trial = False
                wallet.save()
                profile.save()
                transaction = Transaction.objects.create(wallet=wallet, amount=amount, type=1)
                transaction.save()
                serializer = self.serializer_class(transaction)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('You have error on your form. Please double check your information and try again',
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(ex)
            return Response("Failed", status=status.HTTP_400_BAD_REQUEST)


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
        # check users Active subscription
        active_subscriptions = Subscription.objects.all().filter(Q(wallet=wallet) & Q(type=1))
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
    # check users Active subscription
    active_subscriptions = Subscription.objects.all().filter(Q(wallet=wallet) & Q(type=1))
    if len(active_subscriptions) > 0:
        for subscription in active_subscriptions:
            # Make subscription type = Canceled
            subscription.type = 3
            subscription.save()
        return Response("Subscription is Canceled", status=status.HTTP_200_OK)
    else:
        return Response("There aren't active subscription", status=status.HTTP_204_NO_CONTENT)
