# Generated by Django 3.0.4 on 2020-05-01 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20200429_0359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
    ]
