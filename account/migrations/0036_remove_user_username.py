# Generated by Django 3.0.4 on 2020-05-14 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0035_auto_20200514_1001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]