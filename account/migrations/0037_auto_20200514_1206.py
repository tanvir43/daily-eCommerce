# Generated by Django 3.0.4 on 2020-05-14 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0036_remove_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(blank=True, null=True, to='account.Role'),
        ),
    ]
