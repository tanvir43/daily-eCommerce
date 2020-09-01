from math import floor, ceil
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
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        fetched_by = request.user
        # try:
        #     user = User.objects.get(id=pk)
        # except Exception:
        #     return Response({'status': 'User not found'}, status=status.HTTP_200_OK)
        # else:
        if fetched_by.is_staff:
            order = Order.objects.all().order_by('-created_at')
            context = {'request': request}
            # order = self.get_queryset()
            page = self.paginate_queryset(order)
            if page is not None:
                serializer = self.serializer_class(order, many=True, context=context)
                return self.get_paginated_response(serializer.data)
            serializer = OrderSerializer(order, many=True, context=context)
            return Response(serializer.data)
        else:
            return Response({'status': 'You are not a staff user'}, status=status.HTTP_200_OK)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


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
                    serializer = self.serializer_class(order, many=True, context=context)
                    return self.get_paginated_response(serializer.data)
                serializer = OrderSerializer(order, many=True, context=context)
                return Response(serializer.data)
                # serializer = self.serializer_class(order, many=True, context=context)
                # return Response(serializer.data)
            else:
                return Response({'status': 'You are not a staff user'}, status=status.HTTP_200_OK)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)