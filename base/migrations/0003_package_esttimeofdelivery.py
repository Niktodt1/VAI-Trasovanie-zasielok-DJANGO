# Generated by Django 4.1.5 on 2023-01-13 10:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_useraccount_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='estTimeOFDelivery',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
