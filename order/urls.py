from django.urls import path

from order import views, admin_views

urlpatterns = [
        path('order/list', views.OrderListAPIView.as_view(), name='order-list'),
        path('order/create', views.OrderCreateAPIView.as_view(), name='order-create'),
        path('order/<str:pk>/detail', views.OrderDetailAPIView.as_view(), name='order-detail'),
        path('order/<str:pk>/update-status', views.OrderStatusUpdateAPI.as_view(), name='order-cancel'),
        path('order/<str:amount>/get-delivery-charge', views.GetDeliveryChargeWithDiscount.as_view(), name='get-delivery-charge'),
        # path('order/<int:pk>/detail', views.OrderDetailAPIView.as_view(), name='order-detail'),
        # path('order/<int:pk>/edit', views.OrderUpdateAPIView.as_view(), name='order-update'),
        # path('order/<int:pk>/delete', views.OrderDeleteAPIView.as_view(), name='order-delete'),


        path('admin/order/list', admin_views.AllOrderListAPIView.as_view(), name='all-order-list'),
        path('admin/order/<str:pk>/user/list', admin_views.UserOrderListAPIView.as_view(), name='user-order-list'),
        path('admin/order/<str:pk>/detail', admin_views.UserOrderDetailAPIView.as_view(), name="user-order-detail"),
        path('admin/order/create', admin_views.UserOrderCreateAPIView.as_view(), name="user-order-create"),
    ]