# Generated by Django 3.2.2 on 2021-07-23 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('league', '0005_team_seed'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='league',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]