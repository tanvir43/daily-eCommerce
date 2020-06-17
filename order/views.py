from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView
    )
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from products.models import Product ,OrderItem
from account.models import User, Address

from .models import Order, Payment, Coupon
from .serializers import OrderSerializer

from django_filters.rest_framework import DjangoFilterBackend


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        order_data = data['order']
        order_data['user'] = request.user.id
        print("order data", order_data)
        shipping_address = order_data['shipping_address']
        status = order_data['status']
        currency = order_data['currency']
        address = Address.objects.get(id=shipping_address)
        order = Order(
            user=user,
            shipping_address=address,
            billing_address=address,
            currency=currency
        )
        order.save()
        # serializer = self.serializer_class(data=order_data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(user=request.user)
        for item in data['items']:
            product = Product.objects.get(slug=item['slug'])
            order_item = OrderItem.objects.create(
                user=user,
                product=product,
                ordered=True,
                quantity=item['quantity']
            )
            order_item.order.add(order)
        return Response(status=status.HTTP_201_CREATED)

        # product_ids = self.request['product_ids']