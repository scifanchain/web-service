# Generated by Django 3.2.6 on 2021-09-25 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0005_wallet_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
