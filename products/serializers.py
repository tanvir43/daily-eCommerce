from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Category, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


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
