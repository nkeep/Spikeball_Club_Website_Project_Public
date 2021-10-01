# Generated by Django 3.2.2 on 2021-07-17 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0002_league_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_number', models.IntegerField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='league',
            name='weeks_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='league',
            name='weeks',
            field=models.ManyToManyField(blank=True, to='league.Week'),
        ),
    ]
