from django.urls import path

from products import views

urlpatterns = [
        # path('product-detail/<int:pk>/', views.product_detail),
        path('list/', views.ProductListAPIView.as_view(), name='list'),
        path('create/', views.ProductCreateAPIView.as_view(), name='create'),
        path('detail/<str:slug>/', views.ProductDetailAPIView.as_view(), name='detail'),
        path('edit/<int:pk>/', views.ProductUpdateAPIView.as_view(), name='update'),
        path('delete/<int:pk>/', views.ProductDetailAPIView.as_view(), name='delete'),
]
