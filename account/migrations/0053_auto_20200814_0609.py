# Generated by Django 3.0.7 on 2020-08-14 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0052_address_updated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]