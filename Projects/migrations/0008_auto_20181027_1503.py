# Generated by Django 2.1.2 on 2018-10-27 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0007_auto_20181026_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='prs',
            name='bonus_points',
            field=models.IntegerField(default=0, verbose_name='bonus_points'),
        ),
        migrations.AddField(
            model_name='prs',
            name='deducted_points',
            field=models.IntegerField(default=0, verbose_name='deducted_points'),
        ),
    ]