# Generated by Django 3.2 on 2022-05-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makematch', '0014_auto_20220511_2357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='walkorver_match',
            new_name='walkover_match',
        ),
        migrations.AlterField(
            model_name='player',
            name='rnd',
            field=models.FloatField(default=0.4750991024179808),
        ),
    ]