# Generated by Django 3.2.6 on 2021-09-18 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0003_rename_public_key_wallet_publickey'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='kind',
            field=models.CharField(default='', max_length=50),
        ),
    ]
