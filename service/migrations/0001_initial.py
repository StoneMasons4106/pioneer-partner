# Generated by Django 4.1.7 on 2023-04-03 22:28

import address.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("address", "0003_auto_20200830_1851"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Call",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=254)),
                ("contact_date", models.DateTimeField()),
                ("notes", models.TextField(blank=True, max_length=3000, null=True)),
                (
                    "address",
                    address.models.AddressField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="address.address",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReturnVisit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("contact_date", models.DateTimeField()),
                ("notes", models.TextField(blank=True, max_length=3000, null=True)),
                (
                    "call",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="service.call"
                    ),
                ),
            ],
        ),
    ]
