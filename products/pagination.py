from rest_framework.pagination import CursorPagination
from django.conf import settings

class ProductCursorPagination(CursorPagination):
    page_size = getattr(settings, 'PRODUCTS_PAGE_SIZE', 10)
    ordering = '-created_at'
    page_size_query_param = 'page_size'
    max_page_size = 50
