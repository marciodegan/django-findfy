# Generated by Django 3.0.9 on 2020-11-24 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantes', '0007_auto_20201124_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurante',
            name='deactivate',
            field=models.BooleanField(default=False, null=True),
        ),
    ]