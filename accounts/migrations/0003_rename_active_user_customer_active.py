# Generated by Django 4.0.4 on 2022-09-06 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_plate_licence_customer_driver_licence_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='active_user',
            new_name='active',
        ),
    ]
