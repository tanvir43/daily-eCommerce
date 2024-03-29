# Generated by Django 3.0.7 on 2020-08-19 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0028_auto_20200819_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverycharge',
            name='discount_range',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='deliverycharge',
            name='flat_discount',
            field=models.IntegerField(default=0, verbose_name='discount percentage'),
        ),
    ]
