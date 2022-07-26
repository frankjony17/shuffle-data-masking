# Generated by Django 3.2.6 on 2021-10-13 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorType',
            fields=[
                ('error_type_id', models.BigAutoField(db_column='ERROR_TYPE_ID', primary_key=True, serialize=False)),
                ('error_type', models.CharField(db_column='ERROR_TYPE', max_length=200)),
                ('error_description', models.CharField(db_column='ERROR_DESCRIPTION', max_length=500)),
                ('created_at_dt', models.DateTimeField(db_column='CREATED_AT_DT')),
                ('created_by_ds', models.CharField(db_column='CREATED_BY_DS', max_length=500)),
            ],
            options={
                'db_table': 'ERROR_TYPE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessError',
            fields=[
                ('process_error_id', models.BigAutoField(db_column='PROCESS_ERROR_ID', primary_key=True, serialize=False)),
                ('error_description', models.CharField(db_column='ERROR_DESCRIPTION', max_length=1000)),
                ('original_query', models.CharField(blank=True, db_column='ORIGINAL_QUERY', max_length=1000, null=True)),
                ('queue_process_id', models.BigIntegerField(db_column='QUEUE_PROCESS_ID')),
                ('created_at_dt', models.DateTimeField(db_column='CREATED_AT_DT')),
                ('created_by_ds', models.CharField(db_column='CREATED_BY_DS', max_length=500)),
            ],
            options={
                'db_table': 'PROCESS_ERROR',
                'ordering': ['process_error_id'],
                'managed': False,
            },
        ),
    ]
