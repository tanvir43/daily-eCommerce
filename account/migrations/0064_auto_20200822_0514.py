# Generated by Django 3.0.7 on 2020-08-22 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0063_address_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]