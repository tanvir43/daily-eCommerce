# Generated by Django 3.0.7 on 2020-08-17 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_auto_20200817_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]