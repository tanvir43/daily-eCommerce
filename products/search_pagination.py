from rest_framework.response import Response

from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from rest_framework.exceptions import APIException
from rest_framework import status


class NotFound(APIException):
    status_code = status.HTTP_200_OK
    default_detail = ('Not found.')
    default_code = 'not_found'


class SearchPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'

    # def paginate_queryset(self, queryset, request, view=None):
    #     """
    #     Paginate a queryset if required, either returning a
    #     page object, or `None` if pagination is not configured for this view.
    #     """
    #     page_size = self.get_page_size(request)
    #     if not page_size:
    #         return None
    #
    #     paginator = self.django_paginator_class(queryset, page_size)
    #     page_number = request.query_params.get(self.page_query_param, 1)
    #     if page_number in self.last_page_strings:
    #         page_number = paginator.num_pages
    #
    #     try:
    #         self.page = paginator.page(page_number)
    #     except Exception as exc:
    #         # msg = self.invalid_page_message.format(
    #         #     page_number=page_number, message=str(exc)
    #         # )
    #         msg = {
    #             'next': "null",
    #             'previous': "null",
    #             'count': 0,
    #             'limit': 0,
    #             'results': []
    #         }
    #         raise NotFound(msg)
    #
    #     if paginator.num_pages > 1 and self.template is not None:
    #         # The browsable API should display pagination controls.
    #         self.display_page_controls = True
    #
    #     self.request = request
    #     return list(self.page)
    #
    # def get_paginated_response(self, data):
    #     if len(data) > 0:
    #         return Response({
    #             'next': self.get_next_link(),
    #             'previous': self.get_previous_link(),
    #             'count': self.page.paginator.count,
    #             'limit': self.page_size,
    #             'results': data
    #         })
    #     else:
    #         return Response({
    #             'next': self.get_next_link(),
    #             'previous': self.get_previous_link(),
    #             'count': self.page.paginator.count,
    #             'limit': self.page_size,
    #             'results': []
    #         })