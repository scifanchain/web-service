# Generated by Django 3.2.6 on 2021-10-07 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0014_auto_20211007_0240'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstage',
            name='coin',
            field=models.BigIntegerField(default=0, verbose_name='通证'),
        ),
        migrations.AddField(
            model_name='historicalstage',
            name='proofed',
            field=models.BooleanField(default=False, verbose_name='是否存证'),
        ),
        migrations.AddField(
            model_name='stage',
            name='coin',
            field=models.BigIntegerField(default=0, verbose_name='通证'),
        ),
        migrations.AddField(
            model_name='stage',
            name='proofed',
            field=models.BooleanField(default=False, verbose_name='是否存证'),
        ),
    ]
