# Generated by Django 4.0 on 2022-11-25 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='url',
            field=models.URLField(default='https://www.google.com/', max_length=1024),
            preserve_default=False,
        ),
    ]
