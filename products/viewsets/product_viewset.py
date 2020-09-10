from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet, DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination, LimitOffsetPagination
from products.search_pagination import SearchPageNumberPagination
# SearchPageNumberPagination

from ..documents.product import ProductDocument
from ..search_serializers.product import ProductDocumentSerializer
from json import JSONEncoder
from rest_framework.renderers import JSONRenderer


class JSONSearchEncoder(JSONEncoder):
    def default(self, obj):
        from elasticsearch_dsl.response import Hit
        if isinstance(obj, Hit):
            return obj.to_dict()
        return super().default(obj)


class JSONSearchRenderer(JSONRenderer):
    encoder_class = JSONSearchEncoder
#
# class GeneralSearchAPIView(APIView):
#     renderer_classes = (JSONSearchRenderer,)


class ProductDocumentView(DocumentViewSet):
    """The Product Document View"""

    document = ProductDocument
    serializer_class = ProductDocumentSerializer
    # renderer_classes = (JSONSearchRenderer,)
    pagination_class = SearchPageNumberPagination #LimitOffsetPagination # #PageNumberPagination #CustomPageNumberPagination #
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        SuggesterFilterBackend,

    ]
    # Define search fields
    # search_fields = {
    #     'name': {'fuzziness': 'AUTO'},
    #     'slug': None,
    #     'price': None,
    # }
    search_fields = (
        'name',
        'slug',
        'price'
    )
    # Define filter fields
    filter_fields = {
        'id': {
            'field': 'id',
            # Note, that we limit the lookups of id field in this example,
            # to `range`, `in`, `gt`, `gte`, `lt` and `lte` filters.
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        # 'name': 'name.raw',
        'name': 'name',
        # 'slug': 'slug.raw',
        'slug': 'slug',
        'description': 'description',
        'created_at': 'created_at',
        'currency': 'currency',
        'available': 'available',
        # 'quantity': 'quantity.raw',
        # 'count_sold': 'count_sold.raw',
        # 'is_deleted': 'is_deleted.raw',
        'price': {
            'field': 'price',
            # Note, that we limit the lookups of `price` field in this
            # example, to `range`, `gt`, `gte`, `lt` and `lte` filters.
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        # 'stock': {
        #     'field': 'stock',
        #     # Note, that we limit the lookups of `stock_count` field in
        #     # this example, to `range`, `gt`, `gte`, `lt` and `lte`
        #     # filters.
        #     'lookups': [
        #         LOOKUP_FILTER_RANGE,
        #         LOOKUP_QUERY_GT,
        #         LOOKUP_QUERY_GTE,
        #         LOOKUP_QUERY_LT,
        #         LOOKUP_QUERY_LTE,
        #     ],
        # },
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        # 'name': 'name.raw',
        'name': 'name',
        # 'slug': 'slug.raw',
        'slug': 'slug',
        'price': 'price',
        # 'created_at': 'created_at',
    }
    # Specify default ordering
    ordering = ('id', 'name')

    suggester_fields = {
        'name_suggest': {
            'field': 'name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'options': {
                'size': 25,  # Override default number of suggestions
                'skip_duplicates': True,  # Whether duplicate suggestions should be filtered out.
            },
        },
    }