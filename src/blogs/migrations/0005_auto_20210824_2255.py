# Generated by Django 3.2.6 on 2021-08-24 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20210824_2252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='created_time',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created_time',
            new_name='created',
        ),
    ]
