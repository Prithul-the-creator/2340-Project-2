from django.contrib.auth.management import create_permissions
from django.db import migrations


def create_recruiter_group(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    recruiter, _ = Group.objects.get_or_create(name='Recruiter')
    recruiter.permissions.add(*Permission.objects.filter(
        content_type__app_label='jobs',
        codename__in=['view_application', 'change_application'],
    ))


def remove_recruiter_group(apps, schema_editor):
    apps.get_model('auth', 'Group').objects.filter(name='Recruiter').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_job_owner'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(create_recruiter_group, remove_recruiter_group),
    ]
