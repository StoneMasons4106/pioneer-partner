# Generated by Django 4.1.9 on 2023-05-19 21:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0007_alter_territory_map"),
    ]

    operations = [
        migrations.AddField(
            model_name="territory",
            name="territory_id",
            field=models.CharField(
                default=9876541234567894, max_length=16, unique=True
            ),
            preserve_default=False,
        ),
    ]
