# Generated by Django 3.0.7 on 2020-08-09 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_order_cancelled_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cancelled_by',
        ),
    ]
