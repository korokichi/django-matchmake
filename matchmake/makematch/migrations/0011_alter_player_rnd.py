# Generated by Django 3.2 on 2022-05-10 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makematch', '0010_alter_player_rnd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='rnd',
            field=models.FloatField(default=0.023839751944027543),
        ),
    ]
