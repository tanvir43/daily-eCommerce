from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedIdentityField,
    PrimaryKeyRelatedField
    )

from .models import Order


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"