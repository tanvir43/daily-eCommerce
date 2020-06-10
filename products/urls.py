from django.urls import path

from products import views

urlpatterns = [
        # path('product-detail/<int:pk>/', views.product_detail),
        path('category/list', views.CategoryListAPIView.as_view(), name='category-list'),
        path('category/create', views.CategoryCreateAPIView.as_view(), name='category-create'),
        path('category/<str:slug>/detail', views.CategoryDetailAPIView.as_view(), name='category-detail'),
        path('category/<str:slug>/edit', views.CategoryUpdateAPIView.as_view(), name='category-update'),
        path('category/<str:slug>/delete', views.CategoryDeleteAPIView.as_view(), name='category-delete'),
        path('products/list', views.ProductListAPIView.as_view(), name='product-list'),
        path('products/create', views.ProductCreateAPIView.as_view(), name='product-create'),
        path('products/<str:slug>/detail', views.ProductDetailAPIView.as_view(), name='product-detail'),
        path('products/<str:slug>/edit', views.ProductUpdateAPIView.as_view(), name='product-update'),
        path('products/<str:slug>/delete', views.ProductDetailAPIView.as_view(), name='product-delete'),
        path('unit/list', views.UnitListAPIView.as_view(), name='unit-list'),
        path('unit/create', views.UnitCreateAPIView.as_view(), name='unit-create'),
        path('unit/<str:pk>/detail', views.UnitDetailAPIView.as_view(), name='unit-detail'),
        path('unit/<str:pk>/edit', views.UnitUpdateAPIView.as_view(), name='unit-update'),
        path('unit/<str:pk>/delete', views.UnitDeleteAPIView.as_view(), name='unit-delete'),
]
