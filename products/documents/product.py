from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from elasticsearch_dsl.analysis import (
    CustomAnalyzer,
    CustomTokenizer,
    CustomTokenFilter,
    CustomCharFilter,
)

from ..models import Product

# Name of the Elasticsearch index
# INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES['__name__'])
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES['products.documents.product'])

INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

custom_analyzer = CustomAnalyzer._type_shortcut
custom_tokenizer = CustomTokenizer._type_shortcut
custom_token_filter = CustomTokenFilter._type_shortcut
custom_char_filter = CustomCharFilter._type_shortcut

#Custom analyzer
html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

html_strip_lowercase = custom_analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@INDEX.doc_type
class ProductDocument(Document):
    """
    Product Elasticsearch document
    """
    id = fields.IntegerField(attr='id')
    name = fields.KeywordField(
        # analyzer=html_strip,
        attr='name',
        fields={
            'suggest': fields.CompletionField(),
            # 'lower': fields.KeywordField(analyzer=html_strip_lowercase),
        }
    )
    # name = fields.KeywordField(
    #     analyzer=html_strip,
    #     attr='name',
    #     fields={
    #         'suggest': fields.CompletionField(),
    #         'lower': (analyzer=html_strip_lowercase),
    #     }
    # )
    # name = fields.TextField(
    #     attr='name',
    #     fields={
    #         'suggest': fields.Completion(),
    #     }
    # )
    # name = fields.TextField(
    #     analyzer=html_strip,
    #     fields={
    #         "raw": fields.TextField(analyzer='keyword')
    #         # "raw": fields.KeywordField(),
    #     }
    # )
    slug = fields.KeywordField(
        attr='slug',
        fields={
            'suggest': fields.Completion(),
        }
    )
    # slug = fields.TextField(
    #     attr='slug',
    #     fields={
    #         'suggest': fields.Completion(),
    #     }
    # )
    # slug = fields.TextField(
    #     analyzer=html_strip,
    #     fields={
    #         "raw": fields.TextField(analyzer='keyword')
    #     }
    # )
    # description = fields.TextField(
    #     analyzer=html_strip,
    #     fields={
    #         "raw": fields.TextField(analyzer='keyword')
    #     }
    # )
    # category = fields.TextField(
    #     attr='category_indexing',
    #     analyzer=html_strip,
    #     fields={
    #         "raw": fields.TextField(analyzer='keyword')
    #     }
    # )
    # unit = fields.TextField(
    #     attr='unit_indexing',
    #     analyzer=html_strip,
    #     fields={
    #         "raw": fields.TextField(analyzer='keyword')
    #     }
    # )
    # currency = fields.TextField(
    #     analyzer=html_strip,
    #     fields={
    #         "raw": fields.TextField(analyzer='keyword')
    #     }
    # )
    # created_at = fields.DateField()
    price = fields.FloatField()
    # minimal_variant_price = fields.FloatField()
    available = fields.BooleanField()
    charge_taxes = fields.BooleanField()
    stock = fields.IntegerField()
    count_sold = fields.IntegerField()
    discount_price = fields.IntegerField()
    quantity = fields.IntegerField()
    image = fields.FileField()

    class Django(object):
        """Inner nested class Django."""

        model = Product  # The model associate with this Document
    # class Meta:
    #     model = Product
    #     # fields = [
    #     #     'id',
    #     #     'color',
    #     #     'description',
    #     #     'type',
    #     # ]