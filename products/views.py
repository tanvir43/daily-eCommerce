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
    SearchProductSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    CategorySerializer,
    CategoryListSerializer,
    CategoryChildSerializer,
    CategoryDetailSerializer,
    UnitSerializer
    )
from products.documents.product import ProductDoc
from .search import search
from .pagination import (
    ProductLimitOffsetPagination,
    CustomPageNumberPagination,
    CustomPaginator
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


# product search view
class SearchProductsAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SearchProductSerializer

    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q is not None:
            return search(q)
        return super().get_queryset()


# Another product search view
class SearchProductAPIView(ListAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = SearchProductSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q')
        context = {'request': request}
        ids = []
        if query:
            try:
                s = ProductDoc.search()
                s = s.query('wildcard', name=query)
                response = s.execute()
                response_dict = response.to_dict()
                hits = response_dict['hits']['hits']
                ids = [hit['_source']['id'] for hit in hits]
                queryset = Product.objects.filter(id__in=ids)
                product_list = list(queryset)
                product_list.sort(key=lambda product: ids.index(product.id))

                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.serializer_class(page, many=True, context=context)
                    return self.get_paginated_response(serializer.data)
                serializer = SearchProductSerializer(queryset, many=True, context=context)
                # serializer = SearchProductSerializer(product_list, many=True, context=context)
            except Exception as e:
                print("eee", e)
                products = Product.objects.filter(name__icontains=query)
                page = self.paginate_queryset(products)
                if page is not None:
                    serializer = self.serializer_class(page, many=True, context=context)
                    return self.get_paginated_response(serializer.data)
                serializer = SearchProductSerializer(products, many=True, context=context)
            return Response(serializer.data)


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        if data['quantity'] != 0:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "You have to set quantity more than 0"}, status=status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPageNumberPagination #ProductListLimitOffsetPagination
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
    pagination_class = CustomPageNumberPagination #CustomPaginator
    # lookup_field = "slug"

    def get(self, request, slug):
        product = Product.objects.filter(category__slug=slug)
        context = {'request': request}
        page = self.paginate_queryset(product)
        if page is not None:
            serializer = ProductDetailSerializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        # else:
        #     return Response({
        #         'next': "null",  # self.get_next_link(),
        #         'previous': "null",  # self.get_previous_link(),
        #         'count': 0,
        #         'limit': 0,
        #         'results': []
        #     })
        print("here s here")
        serializer = ProductDetailSerializer(product, many=True, context=context)
        return Response(serializer.data)

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

    # def get(self, request, slug):
    #     product = Product.objects.filter(category__slug=slug)
    #     context = {'request': request}
    #     print("aaa", product)
    #     paginator = self.pagination_class()
    #     serializer = self.serializer_class(context=context)
    #     # response = paginator.generate_response(product, serializer, request)
    #     response = paginator.generate_response(product, ProductDetailSerializer, request)
    #     # serializer = ProductDetailSerializer(product, many=True)
    #     # return Response(self.pagination_class(serializer.data))
    #     return response


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
