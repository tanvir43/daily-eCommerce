# Generated by Django 3.0.7 on 2020-08-17 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0056_auto_20200817_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
