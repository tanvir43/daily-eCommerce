from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from ..models import Product

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES['__name__'])

INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

#Custom analyzer
html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@INDEX.doc_type
class ProductDocument(Document):
    """
    Product Elasticsearch document
    """
    id = fields.IntegerField(attr='id')
    name = fields.TextField(
        analyzer=html_strip,
        fields={
            "raw": fields.TextField(analyzer='keyword')
        }
    )
    slug = fields.TextField(
        analyzer=html_strip,
        fields={
            "raw": fields.TextField(analyzer='keyword')
        }
    )
    description = fields.TextField(
        analyzer=html_strip,
        fields={
            "raw": fields.TextField(analyzer='keyword')
        }
    )
    category = fields.TextField(
        attr='category_indexing',
        analyzer=html_strip,
        fields={
            "raw": fields.TextField(analyzer='keyword')
        }
    )
    unit = fields.TextField(
        attr='unit_indexing',
        analyzer=html_strip,
        fields={
            "raw": fields.TextField(analyzer='keyword')
        }
    )
    currency = fields.TextField(
        analyzer=html_strip,
        fields={
            "raw": fields.TextField(analyzer='keyword')
        }
    )
    created_at = fields.DateField()
    price = fields.FloatField()
    minimal_variant_price = fields.FloatField()
    available = fields.BooleanField()
    charge_taxes = fields.BooleanField()
    stock = fields.IntegerField()
    count_sold = fields.IntegerField()
    discount_price = fields.IntegerField()
    quantity = fields.IntegerField()

    class Django(object):
        """Inner nested class Django."""

        model = Product  # The model associate with this Document