
from django.db import models

from introspection.models import Table


class ErrorType(models.Model):
    error_type_id = models.BigAutoField(
        db_column='ERROR_TYPE_ID', primary_key=True)
    error_type = models.CharField(
        db_column='ERROR_TYPE', max_length=200)
    error_description = models.CharField(
        db_column='ERROR_DESCRIPTION', max_length=500)
    created_at_dt = models.DateTimeField(
        db_column='CREATED_AT_DT')
    created_by_ds = models.CharField(
        db_column='CREATED_BY_DS', max_length=500)

    class Meta:
        managed = False
        db_table = 'ERROR_TYPE'


class ProcessError(models.Model):
    process_error_id = models.BigAutoField(
        db_column='PROCESS_ERROR_ID', primary_key=True)
    table = models.ForeignKey(
        Table, models.DO_NOTHING, db_column='TABLE_ID')
    error_type = models.ForeignKey(
        ErrorType, models.DO_NOTHING, db_column='ERROR_TYPE_ID')
    error_description = models.CharField(
        db_column='ERROR_DESCRIPTION', max_length=1000)
    original_query = models.CharField(
        db_column='ORIGINAL_QUERY', max_length=1000, blank=True, null=True)
    queue_process_id = models.BigIntegerField(db_column='QUEUE_PROCESS_ID')
    created_at_dt = models.DateTimeField(db_column='CREATED_AT_DT')
    created_by_ds = models.CharField(db_column='CREATED_BY_DS', max_length=500)

    class Meta:
        managed = False
        db_table = 'PROCESS_ERROR'
        ordering = ['process_error_id']
