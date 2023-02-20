from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class.
    """

    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'prev': self.page.previous_page_number() if self.page.has_previous() else None,
            'results': data
        })
