# Generated by Django 2.1.2 on 2018-10-28 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0008_auto_20181027_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='prs',
            name='bonus_pts',
            field=models.IntegerField(default=0, verbose_name='bonus_pts'),
        ),
        migrations.AddField(
            model_name='prs',
            name='deducted_pts',
            field=models.IntegerField(default=0, verbose_name='bonus_pts'),
        ),
    ]
