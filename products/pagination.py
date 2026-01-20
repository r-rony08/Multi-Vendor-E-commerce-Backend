from rest_framework.pagination import CursorPagination

class ProductCursorPagination(CursorPagination):
    page_size = 10                  # default items per page
    ordering = '-created_at'        # default order (newest first)
    page_size_query_param = 'page_size'  # client can request custom page size
    max_page_size = 50              # maximum allowed page size
