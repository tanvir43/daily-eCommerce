from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .viewsets.product_viewset import ProductDocumentView

router = DefaultRouter()
books = router.register(r'products',
                        ProductDocumentView,
                        basename='productdocument')

urlpatterns = [
    url(r'^', include(router.urls)),
]