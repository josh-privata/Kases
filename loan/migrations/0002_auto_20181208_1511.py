# Generated by Django 2.0.3 on 2018-12-08 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalloan',
            name='created',
            field=models.DateTimeField(editable=False, help_text='The creation date', verbose_name='Creation Date'),
        ),
        migrations.AlterField(
            model_name='historicalloan',
            name='description',
            field=models.CharField(blank=True, default=None, help_text='(Optional) Enter a description', max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='historicalloan',
            name='modified',
            field=models.DateTimeField(editable=False, help_text='The mdification date', null=True, verbose_name='Modification date'),
        ),
        migrations.AlterField(
            model_name='historicalloan',
            name='private',
            field=models.BooleanField(default=False, help_text='(Optional) Is Private', verbose_name='Private'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='created',
            field=models.DateTimeField(editable=False, help_text='The creation date', verbose_name='Creation Date'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='description',
            field=models.CharField(blank=True, default=None, help_text='(Optional) Enter a description', max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='modified',
            field=models.DateTimeField(editable=False, help_text='The mdification date', null=True, verbose_name='Modification date'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='private',
            field=models.BooleanField(default=False, help_text='(Optional) Is Private', verbose_name='Private'),
        ),
    ]