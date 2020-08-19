# Generated by Django 3.0.7 on 2020-08-17 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_order_delivered_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverycharge',
            name='charge_range',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]