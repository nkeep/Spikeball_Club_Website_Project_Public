# Generated by Django 3.2.2 on 2021-07-14 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_media_thumbnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='link',
            new_name='url',
        ),
        migrations.AlterField(
            model_name='media',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
