from django.urls import path

from account import views, admin_views

urlpatterns = [
        path('user/signup', views.UserRegistrationAPIView.as_view(), name='user-signup'),
        path('user/login', views.UserLoginAPIView.as_view(), name='user-login'),
        path('user/role/create', views.UserRoleCreateAPIView.as_view(), name='user-role-create'),
        path('address/list', views.AddressListAPIView.as_view(), name='address-list'),
        path('address/create', views.AddressCreateAPIView.as_view(), name='address-create'),
        path('address/<str:pk>/detail', views.AddressDetailAPIView.as_view(), name='address-detail'),
        path('address/<str:pk>/edit', views.AddressUpdateAPIView.as_view(), name='address-update'),
        path('address/<str:pk>/delete', views.AddressDeleteAPIView.as_view(), name='address-delete'),

        # path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        # views.activate, name='activate'),
        path('activate/<str:uidb64>/<str:token>/$',views.activate, name='activate'),

        #admin
        path('admin/address/list', admin_views.AddressListAPIView.as_view(), name='address-list'),
        path('admin/address/create', admin_views.AddressCreateAPIView.as_view(), name='address-create'),
        path('admin/address/<str:pk>/detail', admin_views.AddressDetailAPIView.as_view(), name='address-detail'),
        path('admin/address/<str:pk>/edit', admin_views.AddressUpdateAPIView.as_view(), name='address-update'),
        path('admin/address/<str:pk>/delete', admin_views.AddressDeleteAPIView.as_view(), name='address-delete'),
        # path('user/group/create', views.UserGroupCreateAPIView.as_view(), name='user-group-create'),
        # path('category/<str:slug>/detail', views.CategoryDetailAPIView.as_view(), name='category-detail'),
        # path('products/list', views.ProductListAPIView.as_view(), name='product-list'),
        # path('products/create', views.ProductCreateAPIView.as_view(), name='product-create'),
        # path('products/<str:slug>/detail', views.ProductDetailAPIView.as_view(), name='product-detail'),
        # path('products/<str:slug>/edit', views.ProductUpdateAPIView.as_view(), name='product-update'),
        # path('products/<str:slug>/delete', views.ProductDetailAPIView.as_view(), name='product-delete'),
]