# Generated by Django 2.0.3 on 2018-05-26 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteAuthorisationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Note Classification')),
            ],
            options={
                'verbose_name': 'Note Classification',
                'verbose_name_plural': 'Note Classifications',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='NoteCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Note Category')),
            ],
            options={
                'verbose_name': 'Note Category',
                'verbose_name_plural': 'Note Categories',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='NoteClassificationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Note Classification')),
            ],
            options={
                'verbose_name': 'Note Classification',
                'verbose_name_plural': 'Note Classifications',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='NotePriority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Note Priority')),
                ('colour', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Colour')),
            ],
            options={
                'verbose_name': 'Note Priority',
                'verbose_name_plural': 'Note Priorities',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='NoteStatusGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Note Status Group')),
            ],
            options={
                'verbose_name': 'Note Status Group',
                'verbose_name_plural': 'Note Status Groups',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='NoteStatusType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Note Status Type')),
            ],
            options={
                'verbose_name': 'Note Status Type',
                'verbose_name_plural': 'Note Status Types',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='NoteType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Description')),
                ('created', models.DateTimeField(editable=False, verbose_name='Creation date and time')),
                ('modified', models.DateTimeField(editable=False, null=True, verbose_name='Modification date and time')),
                ('title', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Note Type')),
            ],
            options={
                'verbose_name': 'Note Type',
                'verbose_name_plural': 'Note Types',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='note',
            name='assigned_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_assigned_by', to=settings.AUTH_USER_MODEL, verbose_name='Assigned By'),
        ),
        migrations.AddField(
            model_name='note',
            name='assigned_to',
            field=models.ManyToManyField(blank=True, related_name='note_assigned_to', to=settings.AUTH_USER_MODEL, verbose_name='Assigned To'),
        ),
        migrations.AddField(
            model_name='note',
            name='note_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_manager', to=settings.AUTH_USER_MODEL, verbose_name='Note Manager'),
        ),
        migrations.AlterField(
            model_name='note',
            name='image_upload',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Note Note Image'),
        ),
        migrations.AlterField(
            model_name='note',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Note NoteSlug'),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='Note Note Type'),
        ),
        migrations.AddField(
            model_name='notestatusgroup',
            name='Note_status',
            field=models.ManyToManyField(blank=True, to='note.NoteStatusType', verbose_name='Note Status'),
        ),
        migrations.AddField(
            model_name='note',
            name='authorisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='note.NoteAuthorisationType', verbose_name='Note Authorisation'),
        ),
        migrations.AddField(
            model_name='note',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='note.NoteCategory', verbose_name='Note Category'),
        ),
        migrations.AddField(
            model_name='note',
            name='classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='note.NoteClassificationType', verbose_name='Note Classification'),
        ),
        migrations.AddField(
            model_name='note',
            name='priority',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='note.NotePriority', verbose_name='Note Priority'),
        ),
        migrations.AddField(
            model_name='note',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='note.NoteStatusType', verbose_name='Note Status'),
        ),
        migrations.AddField(
            model_name='note',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='note.NoteType', verbose_name='Note Type'),
        ),
    ]