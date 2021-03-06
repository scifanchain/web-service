# Generated by Django 3.2.6 on 2021-09-17 07:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='频道名称')),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('topic_body', models.CharField(max_length=200, verbose_name='内容')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '删除'), (1, '正常'), (2, '冻结')], default=1, verbose_name='状态')),
                ('top', models.BooleanField(blank=True, default=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('channel', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='community.channel', verbose_name='分类')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_body', models.CharField(max_length=500, verbose_name='内容')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '删除'), (1, '正常'), (2, '冻结')], default=1, verbose_name='状态')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.topic', verbose_name='回复主题')),
            ],
            options={
                'verbose_name': '回复',
                'verbose_name_plural': '回复',
            },
        ),
    ]
