# Generated by Django 2.0.3 on 2019-05-04 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='telephone',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='website',
        ),
    ]