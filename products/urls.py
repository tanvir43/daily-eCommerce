from django.urls import path

from products import views

urlpatterns = [
        # path('product-detail/<int:pk>/', views.product_detail),
        path('products/list/', views.ProductListAPIView.as_view(), name='list'),
        path('products/create/', views.ProductCreateAPIView.as_view(), name='create'),
        path('products/<str:slug>/detail/', views.ProductDetailAPIView.as_view(), name='detail'),
        path('products/<int:pk>/edit/', views.ProductUpdateAPIView.as_view(), name='update'),
        path('products/<int:pk>/delete/', views.ProductDetailAPIView.as_view(), name='delete'),
]
