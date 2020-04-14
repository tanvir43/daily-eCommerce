from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class Category(MPTTModel, models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # description_json = JSONField(blank=True, default=dict)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    background_image = models.ImageField(
        upload_to="category-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)
    objects = models.Manager()
    tree = TreeManager()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.children = None

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

#SeoModel, ModelWithMetadata, PublishableModel
class Product(models.Model):
    # product_type = models.ForeignKey(
    #     ProductType, related_name="products", on_delete=models.CASCADE
    # )
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # description_json = SanitizedJSONField(
    #     blank=True, default=dict, sanitizer=clean_draft_js
    # )
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    currency = models.CharField(
        max_length=3,
        default="BDT",
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    # price = MoneyField(amount_field="price_amount", currency_field="currency")
    minimal_variant_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    # minimal_variant_price = MoneyField(
    #     amount_field="minimal_variant_price_amount", currency_field="currency"
    # )
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="product", blank=True, null=True)
    image_alt = models.CharField(max_length=128, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    charge_taxes = models.BooleanField(default=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    # weight = MeasurementField(
    #     measurement=Weight, unit_choices=WeightUnits.CHOICES, blank=True, null=True
    # )
    # objects = ProductsQueryset.as_manager()
    # translated = TranslationProxy()

    class Meta:
        # app_label = "products"
        ordering = ("name",)
        # permissions = (
        #     (ProductPermissions.MANAGE_PRODUCTS.codename, "Manage products."),
        # )\

    def __str__(self):
        return self.name
