from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedIdentityField,
    PrimaryKeyRelatedField
    )

from .models import Category, Product, Unit


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


class ProductListSerializer(ModelSerializer):
    # category = SerializerMethodField()
    # category = CategorySerializer()

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
    products = ProductListSerializer(many=True)
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
            'products'
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

    class Meta:
        model = Category
        fields = [
            'id',
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


class ProductDetailSerializer(ModelSerializer):
    # category = SerializerMethodField()

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
    # def get_category(self, obj):
    #     return str(obj.category.name)
