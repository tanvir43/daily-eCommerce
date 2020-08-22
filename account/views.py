from django.contrib.auth.models import Group
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse

from .utils import random_unique_digits

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

from .tokens import account_activation_token


class UserLoginAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data = self.request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("serialized data", serializer.data)
        if serializer.data['approved']:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {
                'error':  'Please activate your account'
            }
            return Response(error, status=status.HTTP_200_OK)
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


class UserRegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        verification_code = random_unique_digits(5)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(verification_code=verification_code)
        print(user)
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('account_active_email.html', {
            'user': user,
            'verification_code': verification_code,
            # 'domain': current_site.domain,
            # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            # 'token': account_activation_token.make_token(user),
        })
        to_email = data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'A verification code is sent to your email',
        }
        return Response(response, status=status_code)


class UserRoleCreateAPIView(CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = UserRoleSerializer


class UserGroupCreateAPIView(CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = UserGroupSerializer


# class AddressListAPIView(ListAPIView):
#     queryset = Address.objects.filter(deleted=False)
#     serializer_class = AddressSerializer
#     permission_classes = (AllowAny,)


class AddressListAPIView(ListAPIView):
    queryset = Address.objects.filter(deleted=False)
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        address = Address.objects.filter(user=user, deleted=False)
        serializer = self.serializer_class(address, many=True)
        return Response(serializer.data)


class UserActivationAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def patch(self, request, *args, **kwargs):
        data = request.data
        verification_code = data['verification_code']
        email = data['email']
        try:
            user = User.objects.get(email=email)
        except Exception:
            return Response({"error": "User not found with this email"})
        else:
            if user.verification_code == verification_code:
                user.approved = True
                user.verification_code = None
                user.save()
                response = {
                    "status": "Successfully activated"
                }
                return Response(response, status=status.HTTP_200_OK)


class AddressCreateAPIView(CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if Address.objects.filter(is_default=True).exists():
            address = Address.objects.get(is_default=True)
            address.is_default = False
            address.save()
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        response = {
            "id": serializer.data['id'],
            "status": "Address saved successfully"
        }
        return Response(response, status=status.HTTP_201_CREATED)


class AddressDetailAPIView(RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        try:
            address = Address.objects.get(id=pk)
        except Exception as e:
            return Response({"error": "Address not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(address)
            return Response(serializer.data, status=status.HTTP_200_OK)


class AddressUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk, *args, **kwargs):
        try:
            current_address = Address.objects.get(id=pk)
        except Exception as e:
            return Response({"error": "Address not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            if 'is_default' in data and data['is_default']:
                if Address.objects.filter(is_default=True).exists():
                    previous_address = Address.objects.get(is_default=True)
                    previous_address.is_default = False
                    previous_address.save()
            serializer = self.serializer_class(current_address, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {
                "id": serializer.data['id'],
                "status": "Successfully updated"
            }
            return Response(response, status=status.HTTP_200_OK)


class AddressDeleteAPIView(RetrieveUpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        user = request.user
        try:
            address = Address.objects.get(id=pk, deleted=False)
        except Exception as e:
            return Response({"error": "Address not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_address = Address.objects.filter(user=user, deleted=False)
            if 0 < len(user_address) < 2:
                address.deleted = True
                address.is_default = False
                address.save()
                return Response({"status": "address deleted successfully"}, status=status.HTTP_200_OK)
            else:
                if address.is_default:
                    return Response({"status": "As this is your current address, select another address as your current address to remove this address"},
                                    status=status.HTTP_200_OK)
                else:
                    address.deleted = True
                    address.save()
                    return Response({"status": "address deleted successfully"}, status=status.HTTP_200_OK)



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.approved = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


