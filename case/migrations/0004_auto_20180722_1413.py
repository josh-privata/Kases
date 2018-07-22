# Generated by Django 2.0.3 on 2018-07-22 04:13

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0003_auto_20180722_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='case',
            old_name='manager',
            new_name='managed_by',
        ),
        migrations.RenameField(
            model_name='historicalcase',
            old_name='manager',
            new_name='managed_by',
        ),
        migrations.RemoveField(
            model_name='case',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='caseevidence',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='casenote',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='casetask',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='historicalcase',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='historicalcaseevidence',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='historicalcasenote',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='historicalcasetask',
            name='deadline',
        ),
    ]