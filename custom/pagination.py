from rest_framework.pagination import LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response

class LimitOffsetPaginationWithoutCount(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
