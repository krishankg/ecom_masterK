# Generated by Django 2.2.4 on 2019-09-09 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0005_auto_20190907_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressmodel',
            name='billing_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address_model', to='billing.BillingProfile'),
        ),
    ]