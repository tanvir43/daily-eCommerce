# Generated by Django 3.0.7 on 2020-08-17 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0054_auto_20200814_0636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='address',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]