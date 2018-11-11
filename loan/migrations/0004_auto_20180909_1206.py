# Generated by Django 2.0.3 on 2018-09-09 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0003_auto_20180909_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalloanrequest',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='historicalloanrequest',
            name='case',
        ),
        migrations.RemoveField(
            model_name='historicalloanrequest',
            name='device',
        ),
        migrations.RemoveField(
            model_name='historicalloanrequest',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalloanrequest',
            name='loan',
        ),
        migrations.RemoveField(
            model_name='historicalloanrequest',
            name='requested_by',
        ),
        migrations.RemoveField(
            model_name='historicalreturnrequest',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='historicalreturnrequest',
            name='case',
        ),
        migrations.RemoveField(
            model_name='historicalreturnrequest',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalreturnrequest',
            name='loan',
        ),
        migrations.RemoveField(
            model_name='historicalreturnrequest',
            name='requested_by',
        ),
        migrations.RemoveField(
            model_name='loanrequest',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='loanrequest',
            name='case',
        ),
        migrations.RemoveField(
            model_name='loanrequest',
            name='device',
        ),
        migrations.RemoveField(
            model_name='loanrequest',
            name='loan',
        ),
        migrations.RemoveField(
            model_name='loanrequest',
            name='requested_by',
        ),
        migrations.RemoveField(
            model_name='returnrequest',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='returnrequest',
            name='case',
        ),
        migrations.RemoveField(
            model_name='returnrequest',
            name='loan',
        ),
        migrations.RemoveField(
            model_name='returnrequest',
            name='requested_by',
        ),
        migrations.AlterField(
            model_name='historicalloan',
            name='status',
            field=models.CharField(choices=[('PE', 'Pending'), ('AP', 'Approved'), ('RE', 'Rejected'), ('HO', 'On Hold'), ('WI', 'Withdrawn')], default='PE', max_length=2, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('PE', 'Pending'), ('AP', 'Approved'), ('RE', 'Rejected'), ('HO', 'On Hold'), ('WI', 'Withdrawn')], default='PE', max_length=2, verbose_name='Status'),
        ),
        migrations.DeleteModel(
            name='HistoricalLoanRequest',
        ),
        migrations.DeleteModel(
            name='HistoricalReturnRequest',
        ),
        migrations.DeleteModel(
            name='LoanRequest',
        ),
        migrations.DeleteModel(
            name='ReturnRequest',
        ),
    ]
