# Generated by Django 3.0.4 on 2020-05-01 06:42

from django.db import migrations

def add_new_groups_field(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model('account', 'User')
    for user in User.objects.all():
        user.new_groups = user.new_groups
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_remove_user_new_groups'),
    ]

    operations = [
        # migrations.RunPython(add_new_groups_field),
    ]
