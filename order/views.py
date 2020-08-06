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


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        order = Order.objects.filter(user=user, deleted=False).order_by('-created_at')
        serializer = self.serializer_class(order, many=True)
        return Response(serializer.data)


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
        address_id = order_data['address_id']
        try:
            address = Address.objects.get(id=address_id)
        except Exception as e:
            return Response({"error": "address not found"}, status=404)
        else:
            order = Order(
                user=user,
                shipping_address=address,
                billing_address=address,
                currency="BDT",
                total_amount=order_data['total_amount']
            )
        # serializer = self.serializer_class(data=order_data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(user=request.user)
            print("item len", )
            if len(data['items']) >= 1:
                for item in data['items']:
                    product = Product.objects.get(slug=item['slug'])
                    if product:
                        if product.stock >= 1:
                            if item['quantity'] > 1:
                                order_item = OrderItem(
                                    user=user,
                                    product=product,
                                    ordered=True,
                                    quantity=item['quantity'],
                                )
                                # product.stock -= item['quantity']
                                # product.save()
                                # order_item.save()
                                # order_item.order.add(order)
                            else:
                                order_item = OrderItem(
                                    user=user,
                                    product=product,
                                    ordered=True,
                                    quantity=1,
                                )
                            product.stock -= item['quantity']
                            product.save()
                            order.save()
                            order_item.save()
                            order_item.order.add(order)
                return Response({"status": "order successfully placed"}, status=201)
            else:
                return Response({"error": "Please select an item"}, status=400)


        # product_ids = self.request['product_ids']


class OrderCancelAPI(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return Order.objects.get(pk=pk)

    def patch(self, request, pk):
        order = self.get_object(pk=pk)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)
