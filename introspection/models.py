from django.db import models


class Database(models.Model):
    database_name = models.CharField(max_length=200)
    process_started = models.BooleanField(default=False)
    constraint_disabled = models.BooleanField(default=False)
    reduction_started = models.BooleanField(default=False)


class Table(models.Model):
    table_name = models.CharField(max_length=200)
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    has_mask = models.BooleanField(default=False)
    was_reduced = models.BooleanField(default=False)


class Column(models.Model):
    column_name = models.CharField(max_length=200)
    type_of_mask = models.SmallIntegerField(default=0)
    primary_key = models.BooleanField(default=False)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)


class RelativeTable(models.Model):
    principal_table = models.ForeignKey(
        Table, related_name="principal_table", on_delete=models.CASCADE, blank=False, null=False)
    principal_column_name = models.ForeignKey(
        Column, related_name="principal_column_name", on_delete=models.CASCADE, blank=False, null=False)
    secondary_table = models.ForeignKey(
        Table, related_name="secondary_table", on_delete=models.CASCADE, blank=False, null=False)
    secondary_column_name = models.ForeignKey(
        Column, related_name="secondary_column_name", on_delete=models.CASCADE, blank=False, null=False)
