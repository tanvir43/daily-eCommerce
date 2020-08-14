# Generated by Django 3.0.7 on 2020-08-09 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0012_auto_20200809_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cancelled_by',
            field=models.ForeignKey(default=66, on_delete=django.db.models.deletion.CASCADE, related_name='cancelled_orders', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]