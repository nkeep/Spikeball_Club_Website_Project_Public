# Generated by Django 3.2.2 on 2021-07-18 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0004_auto_20210717_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='seed',
            field=models.IntegerField(default=0),
        ),
    ]
