"""dailyecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt import views as jwt_views

# from rest_framework_swagger.views import get_swagger_view

from django.views.decorators.csrf import csrf_exempt
# from graphene_django.views import GraphQLView

# schema_view = get_swagger_view(title="dailyecommerce api's")

from .yasg import urlpatterns as url_doc

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from products import search_urls as search_index_urls
#
# urlpatterns = [
#     # ...
#     # Search URLs
#     url(r'^search/', include(search_index_urls)),
#     # ...
# ]

schema_view = get_schema_view(
   openapi.Info(
      title="DailyEcommerceAPI",
      default_version='v1',
      description="Test description",
      # terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('api-documentation', schema_view),
    # re_path('api/(?P<version>(v1|v2))/',include('products.urls')),
    path('admin/', admin.site.urls),
    # path('search/', include(search_index_urls)),
    path('api/', include('products.urls')),
    path('api/', include('account.urls')),
    path('api/', include('order.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += url_doc
