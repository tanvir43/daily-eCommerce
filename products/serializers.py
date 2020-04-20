from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedIdentityField,
    )

from .models import Category, Product


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(ModelSerializer):
    category = SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'description',
            'parent',
            'background_image',
            'background_image_alt',
            'category'
        ]

    def get_category(self, obj):
        if not obj.is_parent:
            return obj.parent.name
        return None


class CategoryListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = [
            'url',
            'name',
            'slug',
            'description',
            'parent',
            'background_image',
            'background_image_alt'
        ]


class CategoryChildSerializer(ModelSerializer):
    sub_category = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'parent',
            'background_image',
            'background_image_alt',
            'sub_category',
        ]


class CategoryDetailSerializer(ModelSerializer):
    sub_category = SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'description',
            'background_image',
            'background_image_alt',
            'sub_category'
        ]

    def get_sub_category(self, obj):
        if obj.is_parent:
            return CategoryChildSerializer(obj.sub_category, many=True).data
        return None


class ProductListSerializer(ModelSerializer):
    # category = SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'category',
            'unit',
            'price',
            'minimal_variant_price',
            'description',
            'currency',
            'available',
            'stock',
            'created_at',
            'updated_at',
            'image',
            'image_alt',
            'charge_taxes'
        ]
    # def get_category(self, obj):
    #     return str(obj.category.name)


class ProductDetailSerializer(ModelSerializer):
    # category = SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'category',
            'unit',
            'price',
            'minimal_variant_price',
            'description',
            'currency',
            'available',
            'stock',
            'created_at',
            'updated_at',
            'image',
        ]
    # def get_category(self, obj):
    #     return str(obj.category.name)
