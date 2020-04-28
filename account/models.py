import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, Group
from django.forms.models import model_to_dict

from django_countries.fields import Country, CountryField
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField


# class RoleName(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name

class User(AbstractUser):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )

    def __str__(self):
        return self.get_full_name()


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
    user = models.ManyToManyField(User)

    def __str__(self):
        # return self.get_id_display()
        return self.name


# class User(AbstractUser):
#     groups = models.ForeignKey(Group, on_delete=models.CASCADE)
#     roles = models.ManyToManyField(Role)
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True
#         )
#
#     def __str__(self):
#         return self.get_full_name()


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
    # phone_number = PhoneNumberField(max_length=10, unique=True, null=False, blank=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "profile"


class Address(models.Model):
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    company_name = models.CharField(max_length=256, blank=True)
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    city_area = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = CountryField()
    country_area = models.CharField(max_length=128, blank=True)
    phone = PhoneNumberField(blank=True, default="")

    # objects = AddressQueryset.as_manager()

    class Meta:
        ordering = ("pk",)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        if self.company_name:
            return "%s - %s" % (self.company_name, self.full_name)
        return self.full_name

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return self.as_data() == other.as_data()

    __hash__ = models.Model.__hash__

    def as_data(self):
        """Return the address as a dict suitable for passing as kwargs.

        Result does not contain the primary key or an associated user.
        """
        data = model_to_dict(self, exclude=["id", "user"])
        if isinstance(data["country"], Country):
            data["country"] = data["country"].code
        if isinstance(data["phone"], PhoneNumber):
            data["phone"] = data["phone"].as_e164
        return data

    def get_copy(self):
        """Return a new instance of the same address."""
        return Address.objects.create(**self.as_data())
