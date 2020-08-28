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
    UserListSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserRoleSerializer,
    UserGroupSerializer,
    AddressSerializer
    )


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user =request.user
        data = request.data
        if user.is_staff:
            if data['approved'] or data['is_superuser']:
                if user.is_superuser:
                    serializer = self.serializer_class(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(created_by=user.email)
                    response = {
                        "id": serializer.data['id'],
                        "status": "User created successfully"
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    response = {
                        "error": "You are not authorized to make an user superuser or approved"
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(created_by=user.email)
                response = {
                    "id": serializer.data['id'],
                    "status": "User created successfully"
                }
                return Response(response, status=status.HTTP_200_OK)

        else:
            return Response({"error": "You are not a staff user"}, status=status.HTTP_201_CREATED)


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        type = kwargs['type']
        if type == 'customer':
            data = User.objects.filter(is_staff=False)
        elif type == 'staff':
            data = User.objects.filter(is_staff=True)
        if user.is_staff:
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {
                'error': 'You are not a staff user'
            }
            return Response(error, status=status.HTTP_200_OK)


class StaffLoginAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data = self.request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("serialized data", serializer.data)
        if serializer.data['is_staff']:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {
                'error':  'You are not a staff user'
            }
            return Response(error, status=status.HTTP_200_OK)


class UserDetailAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            data = User.objects.get(id=pk)
        except Exception:
            return Response({"status": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            if user.is_staff:
                serializer = self.serializer_class(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                error = {
                    'error': 'You are not a staff user'
                }
                return Response(error, status=status.HTTP_200_OK)


class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk, *args, **kwargs):
        user = request.user
        data = request.data
        try:
            target_user = User.objects.get(id=pk)
        except Exception:
            return Response({"status": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            if user.is_staff:
                if user.is_superuser:
                    serializer = self.serializer_class(target_user,
                                                       data=data,
                                                       partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(updated_by=user.email)
                    response = {
                        "id": serializer.data['id'],
                        "data": serializer.data,
                        "status": "User updated successfully"
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    if ('approved' in data and data['approved']) or ('is_superuser' in data and data['is_superuser']):
                        response = {
                            "error": "You are not authorized to make an user superuser or approved"
                        }
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    elif 'email' in data:
                        response = {
                            "error": "You are not authorized change or update email"
                        }
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    elif user == target_user:
                        response = {
                            "error": "You can not modify your own data"
                        }
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        serializer = self.serializer_class(target_user,
                                                           data=data,
                                                           partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save(updated_by=user.email)
                        response = {
                            "id": serializer.data['id'],
                            "data": serializer.data,
                            "status": "User updated successfully"
                        }
                        return Response(response, status=status.HTTP_200_OK)

                # >>>>>>>>N.B: OLD LOGIC STATRS HERE<<<<<<<<
                # if data['approved'] or data['is_superuser']:
                #     if user.is_superuser:
                #         serializer = self.serializer_class(user,
                #                                            data=data,
                #                                            partial=True)
                #         serializer.is_valid(raise_exception=True)
                #         serializer.save(updated_by=user.email)
                #         response = {
                #             "id": serializer.data['id'],
                #             "status": "User updated successfully"
                #         }
                #         return Response(response, status=status.HTTP_200_OK)
                #     else:
                #         response = {
                #             "error": "You are not authorized to make an user superuser or approved"
                #         }
                #         return Response(response, status=status.HTTP_400_BAD_REQUEST)
                # else:
                #     serializer = self.serializer_class(user,
                #                                        data=data,
                #                                        partial=True)
                #     serializer.is_valid(raise_exception=True)
                #     serializer.save(updated_by=user.email)
                #     response = {
                #         "id": serializer.data['id'],
                #         "status": "User updated successfully"
                #     }
                #     return Response(response, status=status.HTTP_200_OK)

            else:
                return Response({"error": "You are not a staff user"}, status=status.HTTP_201_CREATED)


class StaffRoleListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        data = Role.objects.all()
        if user.is_staff:
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {
                'error': 'You are not a staff user'
            }
            return Response(error, status=status.HTTP_200_OK)


class StaffRoleCreateAPIView(CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        if user.is_superuser:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid user request"}, status=status.HTTP_400_BAD_REQUEST)


class StaffGroupListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        data = Group.objects.all()
        if user.is_staff:
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {
                'error': 'You are not a staff user'
            }
            return Response(error, status=status.HTTP_200_OK)


class StaffGroupCreateAPIView(CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        if user.is_superuser:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid user request"}, status=status.HTTP_400_BAD_REQUEST)


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