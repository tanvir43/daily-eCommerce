from django.contrib import admin

from .models import Order, Payment, Coupon, DeliveryCharge

admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(DeliveryCharge)

# Register your models here.
