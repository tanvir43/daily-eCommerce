from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, update_last_login ,Permission
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField

from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

from .models import Address, Role, User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRoleSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    # def to_representation(self, value):
    #     return value.name

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
        )


class UserGroupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
        )


class UserRoleNestedSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    # def to_representation(self, value):
    #     return value.name

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
        )


class UserGroupNestedSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
        )


class PermissionSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Permission
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializers registration requests and creates a new user.
    """

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(read_only=True)

    roles = UserRoleNestedSerializer(
        many=True,
        queryset=Role.objects.all()
    )
    groups = UserGroupNestedSerializer(
        many=True,
        queryset=Group.objects.all()
    )
    # permission = PermissionSerializer(
    #     many=True,
    #     queryset= Permission.objects.all()
    # )

    # role_name = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'groups',
            'roles',
            # 'permission',
            'phone',
            'email',
            'password',
            'token',
            'terms',
            'is_staff',
            'approved',
            'is_superuser',
            'first_name',
            'last_name',
            'username',
            'email',
        )

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    # def create(self, validated_data):
    #     print("VL DATA", validated_data)
    #     # print('group data rrr', validated_data.pop('groups'))
    #     groups = validated_data.pop('groups')
    #     roles = validated_data.pop('roles')
    #
    #     password = validated_data.pop('password')
    #     # permission = Permission.objects.get(name=validated_data.pop('permission', None))
    #     # groups = Group.objects.get(name=validated_data.pop('groups', None))
    #     # roles = Role.objects.get(name=validated_data.pop('roles', None))
    #     user = User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         phone=validated_data['phone'],
    #         # passsword=validated_data['password']
    #     )
    #     if groups:
    #         user.groups.add(groups)
    #     if roles:
    #         user.roles.add(roles)
    #     # if permission:
    #     #     user.has_perm(permission)
    #     # if password is not None:
    #     user.set_password(password)
    #     user.save()
    #
    #     return user
        # extra_kwargs = {'password': {'write_only': True}}
    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)

    # def get_group_name(self, obj):
    #     if obj.groups:
    #         return obj.groups.name
    #     return None


class UserLoginSerializer(serializers.Serializer):
    # username = serializers.CharField(max_length=255, read_only=True)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    approved = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to sign in'
            )

        # Raise an exception if an
        # email is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password required to sign in'
            )

        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # we can also apply this
        # try:
        #     user = authenticate(email=email, password=password)
        # except User.DoesNotExist:
        #     raise serializers.ValidationError(
        #         'User with given email and password does not exists'
        #     )

        # if user in None:
        #     raise serializers.ValidationError(
        #         'A user with this email and password is not found.'
        #     )
        # try:
        # payload = JWT_PAYLOAD_HANDLER(user)
        # jwt_token = JWT_ENCODE_HANDLER(payload)
        # update_last_login(None, user)
        # except User.DoesNotExist:
        #     raise serializers.ValidationError(
        #         'User with given email and password does not exists'
        #     )
        return {
            # 'username': user.username,
            'email': user.email,
            'token': user.token,
            'approved': user.approved,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        }


    # def get_role_name(self, obj):
    #     names = []
    #     roles = obj.roles.get_queryset()
    #     for role in roles:
    #         names.append(role)
    #     return names

        # def create(self, validated_data):
        #     profile_data = validated_data.pop('profile')
        #     role = validated_data.pop
        #     user = User.objects.create_user(**validated_data)
        #     UserProfile.objects.create(
        #         user=user,
        #         first_name=profile_data['first_name'],
        #         last_name=profile_data['last_name'],
        #         phone_number=profile_data['phone_number'],
        #         age=profile_data['age'],
        #         gender=profile_data['gender']
        #     )
        #     return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "user",
            "name",
            "company_name",
            "address",
            "city",
            "postal_code",
            "country",
            "phone",
            "area",
            "deleted",
            "is_default"
        )
