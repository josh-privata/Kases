# Generated by Django 2.0.3 on 2018-08-12 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20180812_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalloan',
            name='case_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='case_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Case'),
        ),
    ]
