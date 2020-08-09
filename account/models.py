import uuid
import jwt

from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    Group,
    AbstractUser,
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    )
from django.forms.models import model_to_dict

from django_countries.fields import Country, CountryField
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField

from commons.abstract import DateTimeModel


class Role(models.Model):
    SUPER_ADMIN = 1
    SALES_STAFF = 2
    SALES_MANAGER = 3
    STORE_OWNER = 4
    STORE_ADMIN = 5
    ROLE_CHOICES = (
        (SUPER_ADMIN, 'super_admin'),
        (SALES_STAFF, 'sales_staff'),
        (SALES_MANAGER, 'sales_manager'),
        (STORE_OWNER, 'store_owner'),
        (STORE_ADMIN, 'store_admin'),
    )

    # id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
    name = models.CharField(max_length=100)
    # user = models.ManyToManyField(User)

    def __str__(self):
        # return self.get_id_display()
        return self.name


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None, phone=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, phone=None):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password, phone)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    groups = models.ManyToManyField(Group)
    roles = models.ManyToManyField(Role)
    # username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    is_staff = models.BooleanField(default=False)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)
    terms = models.BooleanField(default=False)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    # objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email, self.pk

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name.
        """
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name.
        """
        return self.first_name

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Address(DateTimeModel):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=256)
    company_name = models.CharField(max_length=256, blank=True, null=True)
    address = models.TextField(max_length=256)
    city = models.CharField(max_length=256, null=True, blank=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(default="Bangladesh", max_length=256)
    phone = PhoneNumberField(max_length=256)
    area = models.CharField(max_length=256)
    deleted = models.BooleanField(default=False)

    # first_name = models.CharField(max_length=256, blank=True, null=True)
    # last_name = models.CharField(max_length=256, blank=True, null=True)
    # apartment_address = models.CharField(max_length=100)
    # street_address = models.CharField(max_length=100)
    # street_address_1 = models.CharField(max_length=256, blank=True, null=True)
    # street_address_2 = models.CharField(max_length=256, blank=True, null=True)
    # address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    # city_area = models.CharField(max_length=128, blank=True)
    # country_area = models.CharField(max_length=128, blank=True, null=True)
    # objects = AddressQueryset.as_manager()

    class Meta:
        ordering = ("pk",)
        verbose_name = "Address"
        verbose_name_plural = "Address's"

    # @property
    # def full_name(self):
    #     return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return f"{self.city}, {self.pk}"

    # def __eq__(self, other):
    #     if not isinstance(other, Address):
    #         return False
    #     return self.as_data() == other.as_data()
    #
    # __hash__ = models.Model.__hash__

    # def as_data(self):
    #     """Return the address as a dict suitable for passing as kwargs.
    #
    #     Result does not contain the primary key or an associated user.
    #     """
    #     data = model_to_dict(self, exclude=["id", "user"])
    #     if isinstance(data["country"], Country):
    #         data["country"] = data["country"].code
    #     if isinstance(data["phone"], PhoneNumber):
    #         data["phone"] = data["phone"].as_e164
    #     return data
    #
    # def get_copy(self):
    #     """Return a new instance of the same address."""
    #     return Address.objects.create(**self.as_data())


# class UserProfile(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     first_name = models.CharField(max_length=50, unique=False)
#     last_name = models.CharField(max_length=50, unique=False)
#     phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
#     # phone = PhoneNumberField(max_length=10, unique=True, null=False, blank=False)
#     age = models.PositiveIntegerField(null=True, blank=True)
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
#
#     class Meta:
#         '''
#         to set table name in database
#         '''
#         db_table = "profile"


# class CustomUserManager(BaseUserManager):
#     """
#     Custom user model manager where email is the unique identifiers
#     for authentication instead of usernames.
#     """
#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a User with the given email and password.
#         """
#         if not email:
#             raise ValueError(_('The Email must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))
#         return self.create_user(email, password, **extra_fields)


# class User(AbstractUser):
#     groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
#     # new_groups = models.ForeignKey(Group, related_name='new_groups', null=True, blank=True, on_delete=models.CASCADE)
#     roles = models.ManyToManyField(Role, related_name='roles')
#     username = models.CharField(max_length=100, blank=True, null=True)
#     phone = PhoneNumberField(unique=True)
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True
#         )
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#     objects = CustomUserManager()
#
#     def __str__(self):
#         return self.email
