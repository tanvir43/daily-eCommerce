# Generated by Django 3.0.7 on 2020-08-18 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0024_auto_20200817_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='deliverycharge',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='refund',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]