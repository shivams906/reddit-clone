# Generated by Django 3.1.3 on 2020-11-18 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20201118_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='downs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='post',
            name='ups',
            field=models.IntegerField(default=0),
        ),
    ]