import time
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from elasticsearch_dsl import Search, Index, connections
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from products.models import Product
from products.documents.product import ProductDoc


class Command(BaseCommand):
    help = 'Indexes Skills in Elastic Search'

    def handle(self, *args, **options):
        print("HOST", str(settings.ES_HOST))
        es = Elasticsearch(
            # [{'host': settings.ES_HOST, 'port': settings.ES_PORT}],
            [{'host': 'localhost', 'port': '9200'}],
            index=Index(settings.ELASTICSEARCH_INDEX_NAMES['products.documents'])
        )
        product_index = Index(settings.ELASTICSEARCH_INDEX_NAMES['products.documents'])
        product_index.document(ProductDoc)
        if product_index.exists():
            product_index.delete()
            print('Deleted product index.')
        product_index.create()
        result = bulk(
            client=es,
            actions=(product.product_indexing() for product in Product.objects.all().iterator())
        )
        print('Indexed products')
        print(result)