# Generated by Django 2.2.4 on 2019-09-04 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20190901_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addressmodel',
            old_name='billing_types',
            new_name='address_types',
        ),
    ]