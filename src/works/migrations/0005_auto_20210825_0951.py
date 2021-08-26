# Generated by Django 3.2.6 on 2021-08-25 01:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('works', '0004_auto_20210825_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='作者'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalchapter',
            name='owner',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='belong_to_story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='works.story', verbose_name='所属故事'),
        ),
        migrations.AlterField(
            model_name='historicalchapter',
            name='belong_to_story',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='works.story', verbose_name='所属故事'),
        ),
    ]