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
from products.models import Product
from products.serializers import ProductListSerializer, ProductDetailSerializer, CategorySerializer


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"
    # lookup_url_kwarg = "abc"


class ProductUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

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
