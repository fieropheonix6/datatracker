# Generated by Django 2.2.28 on 2022-12-05 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0029_use_timezone_now_for_person_models'),
        ('mailinglists', '0002_auto_20190703_1344'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Whitelisted',
            new_name='Allowlisted',
        ),
        migrations.AlterModelOptions(
            name='allowlisted',
            options={'verbose_name_plural': 'Allowlisted'},
        ),
    ]