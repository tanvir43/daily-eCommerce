# Generated by Django 3.0.4 on 2020-04-27 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]