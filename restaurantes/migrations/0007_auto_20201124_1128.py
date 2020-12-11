# Generated by Django 3.0.9 on 2020-11-24 14:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurantes', '0006_auto_20201122_2245'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='restaurante',
            unique_together={('user', 'name')},
        ),
    ]