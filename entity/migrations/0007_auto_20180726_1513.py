# Generated by Django 2.0.3 on 2018-07-26 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0006_auto_20180726_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='location',
        ),
        migrations.RemoveField(
            model_name='email',
            name='primary',
        ),
    ]
