# Generated by Django 3.2.6 on 2021-09-12 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumb',
            field=models.ImageField(blank=True, height_field='thumb_height', upload_to='blogs/thumbs', verbose_name='封面图', width_field='thumb_width'),
        ),
        migrations.AddField(
            model_name='post',
            name='thumb_height',
            field=models.PositiveIntegerField(default=90),
        ),
        migrations.AddField(
            model_name='post',
            name='thumb_width',
            field=models.PositiveIntegerField(default=160),
        ),
    ]