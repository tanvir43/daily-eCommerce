import json

from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents.product import ProductDocument


class ProductDocumentSerializer(DocumentSerializer):
    """
    Serializer for Product Document
    """
    class Meta(object):
        """
        Meta options.
        """

        # Specify the correspondent document class
        document = ProductDocument

        # Specify the 
        fields = (
            'name',
            'slug',
            'description',
            'category',
            'currency',
            'price',
            'minimal_variant_price',
            'available',
            'stock',
            'charge_taxes',
            'unit',
            'count_sold',
            'discount_price',
            'quantity'
        )