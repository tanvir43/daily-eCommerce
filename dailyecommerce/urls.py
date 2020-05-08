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

urlpatterns = [
    # path('api-documentation', schema_view),
    path('admin/', admin.site.urls),
    # re_path('api/(?P<version>(v1|v2))/',include('products.urls')),
    path('api/', include('products.urls')),
    path('api/', include('account.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
