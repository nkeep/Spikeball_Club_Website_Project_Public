# Generated by Django 3.2.2 on 2021-07-13 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_delete_photogallery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='photo',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
