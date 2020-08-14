# Generated by Django 3.0.7 on 2020-08-14 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0053_auto_20200814_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
