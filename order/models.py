from uuid import uuid4

from django.db import models

from account.models import User, Address

from commons.abstract import DateTimeModel
from commons.choices import OrderStatus

# Create your models here.


class Order(DateTimeModel):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    cancelled_by = models.ForeignKey(User, related_name="cancelled_orders", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=32, default=OrderStatus.PENDING, choices=OrderStatus.CHOICES
    )
    currency = models.CharField(
        max_length=30,
        default="BDT",
    )
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    token = models.CharField(max_length=36, unique=True, blank=True, null=True)
    # Token of a checkout instance that this order was created from
    checkout_token = models.CharField(max_length=36, blank=True, null=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=15)

    def __str__(self):
        return self.status

    def get_total(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    # def save(self, *args, **kwargs):
    #     if not self.token:
    #         self.token = str(uuid4())
    #     return super(*args, **kwargs)


class Payment(DateTimeModel):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=100)
    payment_via = models.CharField(max_length=100, null=True, blank=True)
    trxid = models.CharField(max_length=256, null=True, blank=True)
    amount = models.FloatField()

    def __str__(self):
        return self.payment_method


class Coupon(models.Model):
    code = models.CharField(max_length=15) #Todo may the `code` should be unique
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"