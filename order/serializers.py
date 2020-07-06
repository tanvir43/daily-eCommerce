from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedIdentityField,
    PrimaryKeyRelatedField
    )

from account.serializers import AddressSerializer
from products.serializers import OrderItemSerializer

from .models import Order


class OrderSerializer(ModelSerializer):
    shipping_address = AddressSerializer()
    billing_address = AddressSerializer()
    email = SerializerMethodField()
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    def get_total_amount(self, obj):
        return obj.get_total()

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Order
        fields = (
            'id',
            'created_at',
            'updated_at',
            "status",
            "currency",
            "being_delivered",
            "received",
            "shipping_address",
            "billing_address",
            "email",
            "order_items",
            "total_amount"
        )