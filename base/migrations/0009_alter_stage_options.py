# Generated by Django 4.1.5 on 2023-01-14 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_package_options_alter_stage_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stage',
            options={'get_latest_by': ['stageCurrentId']},
        ),
    ]
