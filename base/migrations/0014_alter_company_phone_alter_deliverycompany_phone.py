# Generated by Django 4.1.6 on 2023-02-13 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_package_datedelivered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(default='+421##########', max_length=300),
        ),
        migrations.AlterField(
            model_name='deliverycompany',
            name='phone',
            field=models.CharField(default='+421##########', max_length=300),
        ),
    ]
