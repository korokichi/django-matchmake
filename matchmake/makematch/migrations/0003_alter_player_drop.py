# Generated by Django 3.2 on 2022-05-07 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makematch', '0002_tournament_player_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='drop',
            field=models.BooleanField(default=True),
        ),
    ]