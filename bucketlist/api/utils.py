
from rest_framework.pagination import PageNumberPagination


class APIResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 100