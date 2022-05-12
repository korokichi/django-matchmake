# Generated by Django 3.2 on 2022-05-08 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makematch', '0005_player_rnd'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='current_round',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='rnd',
            field=models.FloatField(default=0.5362544090367584),
        ),
    ]
