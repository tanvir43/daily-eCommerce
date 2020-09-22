from math import floor, ceil
from commons.decorator import query_debugger
from django.conf import settings

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
from products.pagination import (
    ProductLimitOffsetPagination,
    CustomPageNumberPagination,
    CustomPaginator
    )
from account.models import User, Address

from .models import Order, Payment, Coupon, DeliveryCharge
from .serializers import OrderSerializer, DeliveryChargeSerializer

from django_filters.rest_framework import DjangoFilterBackend


class AllOrderListAPIView(ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    pagination_class = CustomPageNumberPagination
    # pagination_class = settings.DEFAULT_PAGINATION_CLASS
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        fetched_by = request.user
        # try:
        #     user = User.objects.get(id=pk)
        # except Exception:
        #     return Response({'status': 'User not found'}, status=status.HTTP_200_OK)
        # else:
        if fetched_by.is_staff:
            # order = Order.objects.all().order_by('-created_at')
            context = {'request': request}
            order = self.get_queryset()
            page = self.paginate_queryset(order)
            print("page", page)
            if page is not None:
                serializer = self.serializer_class(page, many=True, context=context)
                return self.get_paginated_response(serializer.data)
            serializer = OrderSerializer(order, many=True, context=context)
            return Response(serializer.data)
        else:
            return Response({'status': 'You are not a staff user'}, status=status.HTTP_200_OK)

    # @property
    # def paginator(self):
    #     """
    #     The paginator instance associated with the view, or `None`.
    #     """
    #     if not hasattr(self, '_paginator'):
    #         if self.pagination_class is None:
    #             self._paginator = None
    #         else:
    #             self._paginator = self.pagination_class()
    #     return self._paginator
    #
    # def paginate_queryset(self, queryset):
    #     """
    #     Return a single page of results, or `None` if pagination is disabled.
    #     """
    #     if self.paginator is None:
    #         return None
    #     return self.paginator.paginate_queryset(queryset, self.request, view=self)
    #
    # def get_paginated_response(self, data):
    #     """
    #     Return a paginated style `Response` object for the given output data.
    #     """
    #     assert self.paginator is not None
    #     return self.paginator.get_paginated_response(data)


class UserOrderListAPIView(ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        fetched_by = request.user
        try:
            user = User.objects.get(id=pk)
        except Exception:
            return Response({'status': 'User not found'}, status=status.HTTP_200_OK)
        else:
            if fetched_by.is_staff:
                context = {'request': request}
                order = Order.objects.filter(user=user).order_by('-created_at')
                page = self.paginate_queryset(order)
                if page is not None:
                    serializer = self.serializer_class(page, many=True, context=context)
                    return self.get_paginated_response(serializer.data)
                serializer = OrderSerializer(order, many=True, context=context)
                return Response(serializer.data)
            else:
                return Response({'status': 'You are not a staff user'}, status=status.HTTP_200_OK)

    # @property
    # def paginator(self):
    #     """
    #     The paginator instance associated with the view, or `None`.
    #     """
    #     if not hasattr(self, '_paginator'):
    #         if self.pagination_class is None:
    #             self._paginator = None
    #         else:
    #             self._paginator = self.pagination_class()
    #     return self._paginator
    #
    # def paginate_queryset(self, queryset):
    #     """
    #     Return a single page of results, or `None` if pagination is disabled.
    #     """
    #     if self.paginator is None:
    #         return None
    #     return self.paginator.paginate_queryset(queryset, self.request, view=self)
    #
    # def get_paginated_response(self, data):
    #     """
    #     Return a paginated style `Response` object for the given output data.
    #     """
    #     assert self.paginator is not None
    #     return self.paginator.get_paginated_response(data)


class UserOrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        created_by = request.user
        order_data = data['order']
        pk = data['user']
        # order_data['user'] =
        print("order data", order_data)
        address_id = order_data['address_id']
        payment_method = order_data['payment_method']
        discount = order_data['discount']
        delivery_charge = order_data['delivery_charge']
        try:
            user = User.objects.get(id=pk)
        except Exception:
            return Response({'status': 'User not found'}, status=status.HTTP_200_OK)
        else:
            if created_by.is_staff:
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
                        payment=payment,
                        discount=discount,
                        delivery_charge=delivery_charge,
                        created_by=created_by
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
                        if order:
                            response = {
                                "id": order.id,
                                "status": "order successfully placed"
                            }
                            return Response(response, status=201)
                        else:
                            response = {
                                "error": "Order not created"
                            }
                            return Response(response, status=400)
                    else:
                        return Response({"error": "Please select an item"}, status=400)


class UserOrderDetailAPIView(RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        fetched_by = request.user
        try:
            order = Order.objects.get(id=pk)
        except Exception as e:
            return Response({"error": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if fetched_by.is_staff:
                context = {'request': request}
                serializer = self.serializer_class(order, context=context)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'You are not a staff user'}, status=status.HTTP_200_OK)