# Generated by Django 3.2.6 on 2021-09-17 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='topic_body',
            field=models.TextField(verbose_name='内容'),
        ),
    ]
