# Generated by Django 4.0 on 2022-12-22 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('congregations', '0003_congregation_friday_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicegroup',
            name='service_group_id',
            field=models.CharField(default=1, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
