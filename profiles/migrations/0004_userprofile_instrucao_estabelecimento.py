# Generated by Django 3.0.9 on 2020-11-23 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20201118_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='instrucao_estabelecimento',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
