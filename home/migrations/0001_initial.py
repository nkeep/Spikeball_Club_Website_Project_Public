# Generated by Django 3.2.2 on 2021-07-07 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=300)),
                ('link', models.URLField()),
                ('credits', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('link', models.URLField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]