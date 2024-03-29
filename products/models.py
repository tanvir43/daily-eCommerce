from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_delete

from account.models import User, Address
from order.models import Order
from products.documents.product import ProductDoc

from commons.abstract import DateTimeModel

# class DateTimeModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
#
#     class Meta:
#         abstract = True


class CategoryManager(models.Manager):
    def all(self):
        qs = super(CategoryManager, self).filter(parent=None)
        return qs


class Category(DateTimeModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # description_json = JSONField(blank=True, default=dict)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="sub_category", on_delete=models.CASCADE
    )
    background_image = models.ImageField(
        upload_to="category-backgrounds"
    )
    background_image_alt = models.CharField(max_length=128, blank=True)
    created_by = models.ForeignKey(User,
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    objects = CategoryManager
    # tree = TreeManager()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.children = None

    class Meta:
        app_label = "products"

    def __str__(self):
        return self.name

    def sub_category(self):
        return Category.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class Unit(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30)
    created_by = models.ForeignKey(User,
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(DateTimeModel):
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
    # created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to="product-images")
    image_alt = models.CharField(max_length=128, blank=True, verbose_name="Image Alt")
    # updated_at = models.DateTimeField(auto_now=True, null=True)
    charge_taxes = models.BooleanField(default=True ,verbose_name='Charge Taxes')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    count_sold = models.BigIntegerField(default=0, verbose_name='Count Sold')
    discount_price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField()
    created_by = models.ForeignKey(User,
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    # weight = MeasurementField(
    #     measurement=Weight, unit_choices=WeightUnits.CHOICES, blank=True, null=True
    # )
    # objects = ProductsQueryset.as_manager()
    # translated = TranslationProxy()

    class Meta:
        app_label = "products"
        ordering = ("name",)
        # permissions = (
        #     (ProductPermissions.MANAGE_PRODUCTS.codename, "Manage products."),
        # )\

    def __str__(self):
        return self.name

    # @property
    # def category_indexing(self):
    #     """Category for indexing.
    #
    #     Used in Elasticsearch indexing.
    #     """
    #     if self.category is not None:
    #         return self.category.name
    #
    # @property
    # def unit_indexing(self):
    #     """Unit for indexing
    #
    #     Used for Elasticsearch indexing
    #     """
    #     if self.unit is not None:
    #         return self.unit.name

    # @property
    def product_indexing(self):
        # ProductDoc.init(index=settings.ELASTICSEARCH_INDEX_NAMES['products.documents']  )
        doc = ProductDoc(
            meta={'id': self.pk},
            name=self.name,
            id=self.pk
        )
        # return doc
        doc.save()
        return doc.to_dict(include_meta=True)


class OrderItem(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ManyToManyField(Order, related_name='order_items')
    product = models.ForeignKey('Product', related_name="order_items", on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()


# def update_search(instance, **kwargs):
#     instance.product_indexing().save()
#
#
# def remove_from_search(instance, **kwargs):
#     instance.product_indexing().delete()
#
#
# post_save.connect(update_search, sender=Product)
# pre_delete.connect(remove_from_search, sender=Product)