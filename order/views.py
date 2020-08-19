from commons.decorator import query_debugger

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

from products.models import Product, OrderItem
from account.models import User, Address

from .models import Order, Payment, Coupon, DeliveryCharge
from .serializers import OrderSerializer, DeliveryChargeSerializer

from django_filters.rest_framework import DjangoFilterBackend


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {'request': request}
        order = Order.objects.filter(user=user).order_by('-created_at')
        serializer = self.serializer_class(order, many=True, context=context)
        return Response(serializer.data)


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(id=pk)
        except Exception as e:
            return Response({"error": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {'request': request}
            serializer = self.serializer_class(order, context=context)
            return Response(serializer.data, status=status.HTTP_200_OK)


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
        payment_method = order_data['payment_method']
        if payment_method == "cash":
            payment = Payment.objects.create(
                user=user,
                payment_method=payment_method,
                amount=order_data['total_amount']
            )
        else:
            pass
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
                total_amount=order_data['total_amount'],
                payment=payment
            )
        # serializer = self.serializer_class(data=order_data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(user=request.user)
            print("item len", )
            if len(data['items']) >= 1:
                for item in data['items']:
                    try:
                        product = Product.objects.get(slug=item['slug'])
                    except Exception as e:
                        print(e)
                    else:
                        if product:
                            if product.stock >= 1:
                                if item['quantity'] > 1:
                                    order_item = OrderItem(
                                        user=user,
                                        product=product,
                                        ordered=True,
                                        quantity=item['quantity'],
                                    )
                                    product.stock -= item['quantity']
                                else:
                                    order_item = OrderItem(
                                        user=user,
                                        product=product,
                                        ordered=True,
                                        quantity=1,
                                    )
                                    product.stock -= 1
                                product.save()
                                order.save()
                                order_item.save()
                                order_item.order.add(order)
                return Response({"status": "order successfully placed"}, status=201)
            else:
                return Response({"error": "Please select an item"}, status=400)


        # product_ids = self.request['product_ids']


class OrderStatusUpdateAPI(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    @query_debugger
    def patch(self, request, pk):
        user = request.user
        data = request.data
        try:
            order = Order.objects.get(id=pk)
        except Exception as e:
            return Response({"error": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if order:
                if data['status'] == 'cancelled':
                    if order.status == 'accepted':
                        return Response({"status": "Order already accepted, can not cancel now"}, status=status.HTTP_200_OK)
                    else:
                        if order.status == 'cancelled':
                            return Response({"status": "This order already cancelled"}, status=status.HTTP_200_OK)
                        elif order.status == 'completed':
                            return Response({"status": "This order already completed"}, status=status.HTTP_200_OK)
                        else:
                            # order_items = Order.objects.select_related('order_items').all()
                            order_items = Order.objects.all()
                            print("order items", order_items)
                            for item in order.order_items.all():
                                item.product.stock += item.quantity
                            order.status = data['status']
                            order.cancelled_by = user
                            order.save()
                            return Response({"status": "Order cancelled successfully"}, status=status.HTTP_200_OK)
                else:
                    order.status = data['status']
                    order.updated_by = user
                    order.save()
                    return Response({"status": f"Updated Order status to {order.status} successfully"}, status=status.HTTP_200_OK)


class GetDeliveryChargeWithDiscount(ListAPIView):
    queryset = DeliveryCharge.objects.all()
    serializer_class = DeliveryChargeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        total_amount = float(kwargs['amount'])
        print("order total amount", total_amount)
        delivery_charge = self.queryset
        serializer = self.serializer_class(delivery_charge[0])
        delivery_charge_res = {}
        if delivery_charge[0].charge_range:
            if delivery_charge[0].charge_range > 0.00:
                print("HEre")
                if total_amount < delivery_charge[0].charge_range:
                    print("now herE")
                    delivery_charge_res['delivery_charge'] = 30.00
                else:
                    delivery_charge_res['delivery_charge'] = 0.00
                delivery_charge_res['charge_range'] = delivery_charge[0].charge_range
                delivery_charge_res['flat_discount'] = delivery_charge[0].flat_discount
                return Response(delivery_charge_res)
        return Response(serializer.data)
