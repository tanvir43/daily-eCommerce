from django.apps import AppConfig
from django.conf import settings

from elasticsearch_dsl import connections


class ProductsConfig(AppConfig):
    name = 'products'

    def ready(self):
        import products.signals
        try:
            connections.create_connection(
                # 'art',
                hosts=[
                    {
                     'host': 'localhost',
                     'port': '9200'
                    }
                ]
            )
        except Exception as e:
            print(e)