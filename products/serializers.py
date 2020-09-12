import base64

from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedIdentityField,
    PrimaryKeyRelatedField
    )

from .models import Category, Product, Unit, OrderItem
from order.models import Order


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        # print("Value", value)
        # print("__Class__", self.parent.parent.__class__(Category.objects.filter(parent=None)))
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
    read_only_fields = ['parent']

    def create(self, validated_data):
        print("Without slug", validated_data)
        resutl = Category.objects.create(**validated_data)
        return resutl

    def get_category(self, obj):
        if not obj.is_parent:
            return obj.parent.name
        return None


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


class SearchProductSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            photo_url = obj.image.url
            # return photo_url
            return request.build_absolute_uri(photo_url)
        return None

    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'description',
            'stock',
            'count_sold',
            'image'
        )

class ProductListSerializer(ModelSerializer):
    # category = SerializerMethodField()
    # category = CategorySerializer()
    unit = SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            # 'category',
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
            'charge_taxes',
            'quantity'
        ]

    def get_unit(self, obj):
        return obj.unit.name
    # def get_category(self, obj):
    #     return str(obj.category.name)


class CategoryListSerializer(ModelSerializer):
    # url = HyperlinkedIdentityField(
    #     view_name='category-detail',
    #     lookup_field='slug'
    # )
    # sub_category = SerializerMethodField()
    # parent = PrimaryKeyRelatedField(queryset=Category.objects.filter(parent=None))
    sub_category = RecursiveSerializer(many=True, read_only=True)
    # products = ProductListSerializer(many=True)
    # products = ProductTestSerializer(source='product.all', many=True)

    # def get_parent(self, instance):
    #     print("instance", instance)
    #     return CategoryChildSerializer(instance.sub_category.filter(parent__isnull=True), many=True).data

    class Meta:
        model = Category
        fields = (
            # 'url',
            'id',
            'name',
            'slug',
            'description',
            'parent',
            'background_image',
            'background_image_alt',
            'sub_category',
            # 'products'
        )

    # def get_products(self, obj):
    #     return obj.products.all()

    # sub_category = SerializerMethodField()
    # sub_category = SubcategorySerializer(many=True, read_only=True)

    # def get_sub_category(self, instance):
    #     return CategoryChildSerializer(instance..filter(parent__isnull=True), many=True).data

    # def get_sub_category(self, obj):
    #     for obj in obj.objects.filter(obj_parent__isnull=True):
    #         print(obj.name)
    #         for child in obj.sub_category.all():
    #             print(child.name)
    #             return child.name


class CategoryDetailSerializer(ModelSerializer):
    sub_category = SerializerMethodField()
    parent = SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'background_image',
            'background_image_alt',
            'sub_category',
            'parent'
        ]

    def get_sub_category(self, obj):
        if obj.is_parent:
            return CategoryChildSerializer(obj.sub_category, many=True).data
        return None

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.name
        else:
            return None


class ProductDetailSerializer(ModelSerializer):
    # category = SerializerMethodField()
    unit = SerializerMethodField()
    image = SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            photo_url = obj.image.url
            # return photo_url
            return request.build_absolute_uri(photo_url)
        return None

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            # 'category',
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
            'quantity'
        ]

    def get_unit(self, obj):
        return obj.unit.name
    # def get_category(self, obj):
    #     return str(obj.category.name)


class OrderItemSerializer(ModelSerializer):
    product = SerializerMethodField()
    price = SerializerMethodField()
    unit = SerializerMethodField()
    image = SerializerMethodField()
    slug = SerializerMethodField()

    def get_slug(self, obj):
        return obj.product.slug

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.product.image:
            photo_url = obj.product.image.url
            return request.build_absolute_uri(photo_url)
        return None

    def get_unit(self, obj):
        return obj.product.unit.name

    def get_price(self, obj):
        return obj.get_final_price()

    def get_product(self, obj):
        return obj.product.name

    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
            'price',
            'unit',
            'slug',
            'image'
        )
