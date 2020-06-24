from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView
    )
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

from products.models import Category, Product, Unit
from products.serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategorySerializer,
    CategoryListSerializer,
    CategoryChildSerializer,
    CategoryDetailSerializer,
    UnitSerializer
    )
from .pagination import (
    ProductLimitOffsetPagination,
    ProductPageNumberPagination
    )

from django_filters.rest_framework import DjangoFilterBackend


class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class CategoryUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = "slug"
    permission_classes = (IsAuthenticated,)


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = "slug"
    permission_classes = (AllowAny,)
    # lookup_url_kwarg = "abc"


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategoryListSerializer
    permission_classes = (AllowAny,)


class CategoryDeleteAPIView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = "slug"
    permission_classes = (IsAuthenticated,)


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (IsAuthenticated,)


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)
    pagination_class = ProductPageNumberPagination #ProductListLimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['price']


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"
    permission_classes = (AllowAny,)
    # lookup_url_kwarg = "abc"


class ProductUnderCategoryListView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = (AllowAny,)
    # lookup_field = "slug"

    def get(self, request, slug):
        product = Product.objects.filter(category__slug=slug)
        print("aaa", product)
        serializer = ProductDetailSerializer(product, many=True)
        return Response(serializer.data)


class UnitListAPIView(ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (AllowAny,)


class UnitCreateAPIView(CreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (IsAuthenticated,)


class UnitDetailAPIView(RetrieveAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (AllowAny,)
    # lookup_url_kwarg = "abc"


class UnitUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (IsAuthenticated,)


class UnitDeleteAPIView(DestroyAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (IsAuthenticated,)


class ProductUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"
    permission_classes = (IsAuthenticated,)

    # def patch(self, request, *args, **kwargs):
    #     print("results", kwargs)
    #     try:
    #         products = Product.objects.get(pk=kwargs['pk'])
    #     except Exception as e:
    #         print(e)
    #     serializer = ProductDetailSerializer(products, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    
    # def get_serializer(self, *args, **kwargs):
    #     kwargs['partial_update'] = True
    #     super(ProductUpdateAPIView, self).get_serializer()


class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"
    permission_classes = (IsAuthenticated,)


# @api_view(['GET', 'POST'])
# @permission_classes((permissions.AllowAny,))
# def product_list(request):
#     """
#     List of all product or create a new product
#     :param request:
#     :return:
#     """
#     if request.method == "GET":
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ProductSerializer(request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
