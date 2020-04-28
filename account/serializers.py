from rest_framework import serializers

from .models import Role, User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'age',
            'gender'
        )


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'name',
            'user'
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    role = UserRoleSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'groups',
            'role',
            'email',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            profile_data = validated_data.pop('profile')
            role = validated_data.pop
            user = User.objects.create_user(**validated_data)
            Role.objects.create(
                user=user,
                name=role['name']
            )
            UserProfile.objects.create(
                user=user,
                first_name=profile_data['first_name'],
                last_name=profile_data['last_name'],
                phone_number=profile_data['phone_number'],
                age=profile_data['age'],
                gender=profile_data['gender']
            )
            return user
