# Generated by Django 3.2.6 on 2021-10-25 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('introspection', '0002_table_was_reduced'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporalPrimaryKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=200)),
                ('primary_key', models.CharField(max_length=200)),
                ('father_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='father_table', to='introspection.table')),
            ],
        ),
    ]
