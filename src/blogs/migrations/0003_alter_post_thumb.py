# Generated by Django 3.2.6 on 2021-09-17 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20210912_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumb',
            field=models.ImageField(blank=True, height_field='thumb_height', upload_to='blogs/thumbs//%Y', verbose_name='封面图', width_field='thumb_width'),
        ),
    ]