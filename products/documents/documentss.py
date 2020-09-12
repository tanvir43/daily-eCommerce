# products/documentss.py

from django.conf import settings
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from ..models import Product

# products = Index(settings.ELASTICSEARCH_INDEX_NAMES['products.documents.products'])
# products.settings(number_of_shards=1, number_of_replicas=0)

@registry.register_document
class ProductDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = settings.ELASTICSEARCH_INDEX_NAMES['products.documents.documents']
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        # The model associated with Elasticsearch document
        model = Product
        # The fields of the model you want to be indexed
        # in Elasticsearch
        fields = (
            'name',
            'slug',
            'description',
            # 'category',
            'price',
            'stock',
            'count_sold',
            'image'
        )