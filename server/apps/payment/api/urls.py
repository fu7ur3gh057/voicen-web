from django.urls import path
from . import views

urlpatterns = [
    path("wallet/", views.GetWalletAPIView.as_view(), name="get_wallet"),
    path("make-transaction/", views.MakeTransactionAPIView.as_view(), name="make_transaction"),
    path("transactions/", views.TransactionListAPIView.as_view(), name="transactions"),
    path("subscribe/", views.SubscribeAPIView.as_view(), name="subscribe"),
]
