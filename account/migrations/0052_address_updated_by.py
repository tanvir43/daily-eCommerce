# Generated by Django 3.0.7 on 2020-08-09 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0051_auto_20200803_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='updated_by',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]