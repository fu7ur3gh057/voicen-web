from rest_framework.pagination import PageNumberPagination


class TransactionPagination(PageNumberPagination):
    page_size = 6
