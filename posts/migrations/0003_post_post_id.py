# Generated by Django 4.0 on 2022-10-24 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_id',
            field=models.CharField(default='0', editable=False, max_length=32),
            preserve_default=False,
        ),
    ]
