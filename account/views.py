from django.contrib.auth.models import Group

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


class UserLoginAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data = self.request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     status_code = status.HTTP_200_OK
    #     response = {
    #         'success': 'True',
    #         'status code': status.HTTP_200_OK,
    #         'message': 'User logged in  successfully',
    #         'token': serializer.data['token'],
    #     }
    #     return Response(response, status=status_code)


class UserRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        print("DATA SHAK", request.data)
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        # response = {
        #     'success': 'True',
        #     'status_code': status_code,
        #     'message': 'Successfully registered'
        # }
        return Response(serializer.data, status=status_code)


class UserRoleCreateAPIView(CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = UserRoleSerializer


class UserGroupCreateAPIView(CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = UserGroupSerializer


class AddressListAPIView(ListAPIView):
    queryset = Address.objects.filter(deleted=False)
    serializer_class = AddressSerializer
    permission_classes = (AllowAny,)


class AddressCreateAPIView(CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)


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


