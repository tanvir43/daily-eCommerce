# Generated by Django 3.0.7 on 2020-08-25 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0067_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_by',
            field=models.EmailField(blank=True, max_length=256, null=True),
        ),
    ]