# Generated by Django 2.0.3 on 2018-07-27 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0012_historicalcompanyauthorisation_historicalcompanycategory_historicalcompanyclassification_historicalc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='company',
        ),
    ]
