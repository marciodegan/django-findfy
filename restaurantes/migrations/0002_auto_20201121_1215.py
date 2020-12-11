# Generated by Django 3.0.9 on 2020-11-21 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurante',
            name='imagem_menu',
            field=models.ImageField(blank=True, default='menu/back1.jpg', null=True, upload_to='menu/'),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='logo',
            field=models.ImageField(blank=True, default='menu/logotipo.png', null=True, upload_to='menu/'),
        ),
    ]