# Generated by Django 3.2 on 2022-05-09 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makematch', '0008_auto_20220508_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='player_A_drop',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='match',
            name='player_A_point',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='player_B_drop',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='match',
            name='player_B_point',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='rnd',
            field=models.FloatField(default=0.2646477653272188),
        ),
    ]
