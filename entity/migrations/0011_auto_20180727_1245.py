# Generated by Django 2.0.3 on 2018-07-27 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entity', '0010_auto_20180726_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Location')),
                ('primary', models.BooleanField(default=False)),
                ('line1', models.CharField(blank=True, max_length=255, null=True)),
                ('line2', models.CharField(blank=True, max_length=255, null=True)),
                ('line3', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('postcode', models.CharField(blank=True, max_length=31)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='HistoricalAddress',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('location', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Location')),
                ('primary', models.BooleanField(default=False)),
                ('line1', models.CharField(blank=True, max_length=255, null=True)),
                ('line2', models.CharField(blank=True, max_length=255, null=True)),
                ('line3', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('postcode', models.CharField(blank=True, max_length=31)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Physical'), (2, 'Postal'), (3, 'Other')])),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Address',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCompanyAddress',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('location', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Location')),
                ('primary', models.BooleanField(default=False)),
                ('line1', models.CharField(blank=True, max_length=255, null=True)),
                ('line2', models.CharField(blank=True, max_length=255, null=True)),
                ('line3', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('postcode', models.CharField(blank=True, max_length=31)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Address',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCountry',
            fields=[
                ('code', models.CharField(db_index=True, max_length=4)),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Country')),
                ('lat', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Latitude')),
                ('lng', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Longtitude')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Country',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalEmail',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('location', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Location')),
                ('primary', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical email',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalNote',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('text', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Note')),
                ('added', models.DateTimeField(null=True, verbose_name='Added')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('author', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Note',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPersonAuthorisation',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('private', models.BooleanField(default=False, verbose_name='Private')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Authorisation')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Person Classification',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPersonCategory',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('private', models.BooleanField(default=False, verbose_name='Private')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Category')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Person Category',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPersonClassification',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('private', models.BooleanField(default=False, verbose_name='Private')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Classification')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Person Classification',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPersonStatus',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('private', models.BooleanField(default=False, verbose_name='Private')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Status')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Person Status',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPersonStatusGroup',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('private', models.BooleanField(default=False, verbose_name='Private')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Status Group')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Person Status Group',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPersonType',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('private', models.BooleanField(default=False, verbose_name='Private')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Type')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Person Type',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPrefix',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=55)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical prefix',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSocial',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('location', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Location')),
                ('primary', models.BooleanField(default=False)),
                ('service', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Social Media Service')),
                ('alias', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Social Media Alias')),
                ('url', models.URLField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical social',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalState',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('short_name', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Abbreviation')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='State')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('country', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='entity.Country')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical State',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTelephone',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('location', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Location')),
                ('primary', models.BooleanField(default=False)),
                ('number', models.CharField(db_index=True, max_length=63)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Fixed'), (2, 'Mobile'), (3, 'Fax')])),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical telephone',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalWebsite',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('location', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Location')),
                ('primary', models.BooleanField(default=False)),
                ('url', models.URLField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical website',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Note')),
                ('added', models.DateTimeField(null=True, verbose_name='Added')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_author', to=settings.AUTH_USER_MODEL, verbose_name='Note Author')),
            ],
            options={
                'verbose_name': 'Note',
                'verbose_name_plural': 'Notes',
            },
        ),
        migrations.RemoveField(
            model_name='historicalcompany',
            name='category',
        ),
        migrations.RemoveField(
            model_name='historicalcompany',
            name='classification',
        ),
        migrations.RemoveField(
            model_name='historicalcompany',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalcompany',
            name='prefix',
        ),
        migrations.RemoveField(
            model_name='historicalcompany',
            name='status',
        ),
        migrations.RemoveField(
            model_name='historicalcompany',
            name='type',
        ),
        migrations.RemoveField(
            model_name='historicalperson',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalperson',
            name='prefix',
        ),
        migrations.RemoveField(
            model_name='company',
            name='addresses',
        ),
        migrations.RemoveField(
            model_name='company',
            name='emails',
        ),
        migrations.RemoveField(
            model_name='company',
            name='telephones',
        ),
        migrations.RemoveField(
            model_name='company',
            name='websites',
        ),
        migrations.AddField(
            model_name='address',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Physical'), (2, 'Postal'), (3, 'Other')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='authorisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='entity.CompanyAuthorisation', verbose_name='Company Authorisation'),
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.ManyToManyField(to='entity.Email', verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='company',
            name='social',
            field=models.ManyToManyField(to='entity.Social', verbose_name='Social'),
        ),
        migrations.AddField(
            model_name='company',
            name='telephone',
            field=models.ManyToManyField(to='entity.Telephone', verbose_name='Telephone'),
        ),
        migrations.AddField(
            model_name='company',
            name='website',
            field=models.ManyToManyField(to='entity.Website', verbose_name='Website'),
        ),
        migrations.AddField(
            model_name='person',
            name='age',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Age'),
        ),
        migrations.AddField(
            model_name='person',
            name='aliases',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Aliases'),
        ),
        migrations.AddField(
            model_name='person',
            name='anniversary',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Anniversary'),
        ),
        migrations.AddField(
            model_name='person',
            name='authorisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='entity.PersonAuthorisation', verbose_name='Person Authorisation'),
        ),
        migrations.AddField(
            model_name='person',
            name='birthday',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Birthday'),
        ),
        migrations.AddField(
            model_name='person',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='entity.PersonCategory', verbose_name='Person Category'),
        ),
        migrations.AddField(
            model_name='person',
            name='classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='entity.PersonClassification', verbose_name='Person Classification'),
        ),
        migrations.AddField(
            model_name='person',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='entity.Company', verbose_name='Company'),
        ),
        migrations.AddField(
            model_name='person',
            name='date_started',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date Started'),
        ),
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Gender'),
        ),
        migrations.AddField(
            model_name='person',
            name='height',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Height'),
        ),
        migrations.AddField(
            model_name='person',
            name='job_title',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Job Title'),
        ),
        migrations.AddField(
            model_name='person',
            name='middle_names',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Middle Names'),
        ),
        migrations.AddField(
            model_name='person',
            name='nickname',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Nickname'),
        ),
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Role'),
        ),
        migrations.AddField(
            model_name='person',
            name='salary',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Salary'),
        ),
        migrations.AddField(
            model_name='person',
            name='slug_middle',
            field=models.SlugField(blank=True, editable=False, null=True, verbose_name='Person Type'),
        ),
        migrations.AddField(
            model_name='person',
            name='social',
            field=models.ManyToManyField(to='entity.Social', verbose_name='Social'),
        ),
        migrations.AddField(
            model_name='person',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='entity.PersonStatus', verbose_name='Person Status'),
        ),
        migrations.AddField(
            model_name='person',
            name='taxfile',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Tax File Number'),
        ),
        migrations.AddField(
            model_name='person',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='entity.PersonType', verbose_name='Person Type'),
        ),
        migrations.AddField(
            model_name='person',
            name='weight',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='person',
            name='addresses',
            field=models.ManyToManyField(to='entity.Address', verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='person',
            name='emails',
            field=models.ManyToManyField(to='entity.Email', verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='notes',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='person',
            name='slug_first',
            field=models.SlugField(blank=True, editable=False, null=True, verbose_name='Person Type'),
        ),
        migrations.AlterField(
            model_name='person',
            name='slug_last',
            field=models.SlugField(blank=True, editable=False, null=True, verbose_name='Person Type'),
        ),
        migrations.AlterField(
            model_name='person',
            name='suffix',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='Suffix'),
        ),
        migrations.AlterField(
            model_name='person',
            name='telephones',
            field=models.ManyToManyField(to='entity.Telephone', verbose_name='Telephone'),
        ),
        migrations.AlterField(
            model_name='person',
            name='websites',
            field=models.ManyToManyField(to='entity.Website', verbose_name='Website'),
        ),
        migrations.DeleteModel(
            name='HistoricalCompany',
        ),
        migrations.DeleteModel(
            name='HistoricalPerson',
        ),
        migrations.AddField(
            model_name='company',
            name='addresse',
            field=models.ManyToManyField(to='entity.CompanyAddress', verbose_name='Address'),
        ),
    ]
