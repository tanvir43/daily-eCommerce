# Generated by Django 3.0.7 on 2020-07-07 12:46

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0046_auto_20200707_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(default='Bang', max_length=2),
        ),
    ]
