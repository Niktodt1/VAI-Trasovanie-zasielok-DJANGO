# Generated by Django 4.1.5 on 2023-01-14 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_company_options_alter_deliverycompany_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='package',
            options={'get_latest_by': 'stageCurrentId'},
        ),
        migrations.AlterModelOptions(
            name='stage',
            options={'get_latest_by': ['datetime']},
        ),
    ]
