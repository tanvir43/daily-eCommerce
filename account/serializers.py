from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Role, User


class UserRoleSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):

    # def to_representation(self, value):
    #     return value.name

    class Meta:
        model = Role
        fields = (
            'name'
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer(required=False)
    # role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)
    roles = UserRoleSerializer(many=True, queryset=Role.objects.all())
    group_name = SerializerMethodField()
    # role_name = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'groups',
            'roles',
            'username',
            'phone',
            'email',
            'password',
            'group_name',
            # 'role_name'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def get_group_name(self, obj):
        if obj.groups:
            return obj.groups.name
        return None

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


# class UserRoleSerializer(serializers.ModelSerializer):
#     user_list = UserRegistrationSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Role
#         fields = (
#             'name',
#             'user_list'
#         )


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = (
#             'first_name',
#             'last_name',
#             'phone_number',
#             'age',
#             'gender'
#         )

