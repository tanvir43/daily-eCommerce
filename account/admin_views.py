from django.contrib.auth.models import Group
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView
    )
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from account.models import Address, Role, User
from account.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserRoleSerializer,
    UserGroupSerializer,
    AddressSerializer
    )


class AddressListAPIView(ListAPIView):
    queryset = Address.objects.filter(deleted=False)
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)


class AddressCreateAPIView(CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({'status': 'Address saved successfully'}, status=status.HTTP_201_CREATED)


class AddressDetailAPIView(RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (AllowAny,)
    # lookup_url_kwarg = "abc"


class AddressUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)


class AddressDeleteAPIView(RetrieveUpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk, *args, **kwargs):
        try:
            address_obj = Address.objects.get(id=pk)
        except Exception as e:
            return Response({"error": "Address not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            address_obj.deleted = True
            address_obj.save()
            return Response({"status": "address deleted successfully"}, status=status.HTTP_200_OK)