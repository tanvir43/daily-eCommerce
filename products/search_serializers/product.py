import json

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents.product import ProductDocument


class ProductDocumentSerializer(DocumentSerializer):
    """
    Serializer for Product Document
    """
    image = SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            photo_url = obj.image
            # return photo_url
            return request.build_absolute_uri(photo_url)
        return None

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
            'quantity',
            'image',
        )