# Generated by Django 3.2.2 on 2021-07-23 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_media_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='media_id',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
