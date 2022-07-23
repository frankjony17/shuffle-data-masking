# Generated by Django 3.2.6 on 2021-10-13 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=200)),
                ('type_of_mask', models.SmallIntegerField(default=0)),
                ('primary_key', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('database_name', models.CharField(max_length=200)),
                ('process_started', models.BooleanField(default=False)),
                ('constraint_disabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=200)),
                ('has_mask', models.BooleanField(default=False)),
                ('database', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='introspection.database')),
            ],
        ),
        migrations.CreateModel(
            name='RelativeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('principal_column_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='principal_column_name', to='introspection.column')),
                ('principal_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='principal_table', to='introspection.table')),
                ('secondary_column_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondary_column_name', to='introspection.column')),
                ('secondary_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondary_table', to='introspection.table')),
            ],
        ),
        migrations.AddField(
            model_name='column',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='introspection.table'),
        ),
    ]