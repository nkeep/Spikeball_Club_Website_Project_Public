# Generated by Django 3.2.2 on 2021-07-17 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0004_tournament_entry_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='tteam',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.paymentoption'),
        ),
        migrations.AlterField(
            model_name='pmatch',
            name='team1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PTeam1', to='tournament.tteam'),
        ),
        migrations.AlterField(
            model_name='pmatch',
            name='team2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PTeam2', to='tournament.tteam'),
        ),
        migrations.AlterField(
            model_name='tmatch',
            name='team1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Team1', to='tournament.tteam'),
        ),
        migrations.AlterField(
            model_name='tmatch',
            name='team2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Team2', to='tournament.tteam'),
        ),
    ]
