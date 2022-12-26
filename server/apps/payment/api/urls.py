from django.urls import path
from . import views

urlpatterns = [
    path("wallet/", views.GetWalletAPIView.as_view(), name="get_wallet"),
    path("transaction/", views.TransactionListAPIView.as_view(), name="transactions"),
    path("transaction/create/", views.MakeTransactionAPIView.as_view(), name="create_transaction"),
    path("transaction/receive/", views.ReceiveTransactionAPIView.as_view(), name="receive_transaction"),
    path("subscription/", views.SubscriptionListAPIView.as_view(), name="subscriptions"),
    path("subscription/create/", views.SubscribeAPIView.as_view(), name="subscribe"),
    path("subscription/cancel/", views.unsubscribe, name="subscribe"),
    path("operation/", views.OperationListAPIView.as_view(), name="operations")
]
