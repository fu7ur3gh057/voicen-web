from rest_framework.pagination import PageNumberPagination


class TranscribePagination(PageNumberPagination):
    page_size = 10
