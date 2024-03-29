# Generated by Django 3.0.4 on 2020-05-06 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_delete_parentcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id_area', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(choices=[('apm', 'Apm'), ('business', 'Business'), ('desarrollo', 'Desarrollo'), ('sistemas', 'Sistemas')], max_length=255)),
            ],
            options={
                'verbose_name': 'Área',
                'verbose_name_plural': 'Áreas',
            },
        ),
        migrations.CreateModel(
            name='Atentusiano',
            fields=[
                ('id_atentusiano', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('correo', models.CharField(max_length=255, unique=True)),
                ('anexo', models.CharField(blank=True, max_length=255, null=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='products.Area')),
            ],
            options={
                'verbose_name': 'Atentusiano',
                'verbose_name_plural': 'Atentusianos',
                'ordering': ['nombre'],
            },
        ),
    ]
