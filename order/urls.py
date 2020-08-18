from django.urls import path

from order import views

urlpatterns = [
        path('order/list', views.OrderListAPIView.as_view(), name='order-list'),
        path('order/create', views.OrderCreateAPIView.as_view(), name='order-create'),
        path('order/<str:pk>/detail', views.OrderDetailAPIView.as_view(), name='order-create'),
        path('order/<str:pk>/update-status', views.OrderStatusUpdateAPI.as_view(), name='order-cancel'),
        # path('order/<int:pk>/detail', views.OrderDetailAPIView.as_view(), name='order-detail'),
        # path('order/<int:pk>/edit', views.OrderUpdateAPIView.as_view(), name='order-update'),
        # path('order/<int:pk>/delete', views.OrderDeleteAPIView.as_view(), name='order-delete'),
    ]