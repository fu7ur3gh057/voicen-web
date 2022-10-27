from rest_framework.pagination import PageNumberPagination


class TransactionPagination(PageNumberPagination):
    page_size = 6


class OperationPagination(PageNumberPagination):
    page_size = 9


class SubscriptionPagination(PageNumberPagination):
    page_size = 6
