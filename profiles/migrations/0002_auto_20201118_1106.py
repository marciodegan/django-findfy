# Generated by Django 3.0.9 on 2020-11-18 14:06

from django.db import migrations
import profiles.formatChecker


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=profiles.formatChecker.ContentTypeRestrictedFileField(blank=True, default='images/avatar.png', null=True, upload_to='images/'),
        ),
    ]