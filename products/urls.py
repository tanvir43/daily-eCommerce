from django.urls import path

from products import views

urlpatterns = [
        # path('product-detail/<int:pk>/', views.product_detail),
        path('category/list', views.CategoryListAPIView.as_view(), name='category-list'),
        path('category/create', views.CategoryCreateAPIView.as_view(), name='category-create'),
        path('category/<int:pk>/detail', views.CategoryDetailAPIView.as_view(), name='category-detail'),
        path('products/list/', views.ProductListAPIView.as_view(), name='product-list'),
        path('products/create/', views.ProductCreateAPIView.as_view(), name='product-create'),
        path('products/<str:slug>/detail/', views.ProductDetailAPIView.as_view(), name='product-detail'),
        path('products/<int:pk>/edit/', views.ProductUpdateAPIView.as_view(), name='product-update'),
        path('products/<int:pk>/delete/', views.ProductDetailAPIView.as_view(), name='product-delete'),
]
