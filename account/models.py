from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.forms.models import model_to_dict

from django_countries.fields import Country, CountryField
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField


# class RoleName(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


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

    def __str__(self):
        # return self.get_id_display()
        return self.name


class User(AbstractUser):
    phone = PhoneNumberField(blank=True, default="")
    roles = models.ManyToManyField(Role)


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
