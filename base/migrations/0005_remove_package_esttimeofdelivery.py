# Generated by Django 4.1.5 on 2023-01-13 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_stage_esttimeodelivery_package_dateoforder_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='estTimeOFDelivery',
        ),
    ]
