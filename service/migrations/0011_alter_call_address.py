# Generated by Django 4.1.9 on 2023-05-26 00:47

import address.models
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("address", "0003_auto_20200830_1851"),
        ("service", "0010_alter_territory_assigned_to_donotcall"),
    ]

    operations = [
        migrations.AlterField(
            model_name="call",
            name="address",
            field=address.models.AddressField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="address.address",
            ),
        ),
    ]
