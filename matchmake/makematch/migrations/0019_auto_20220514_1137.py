# Generated by Django 3.2 on 2022-05-14 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makematch', '0018_auto_20220512_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='rnd',
            field=models.FloatField(default=0.7720930020828978),
        ),
        migrations.AlterField(
            model_name='player',
            name='sowp',
            field=models.IntegerField(default=0),
        ),
    ]
