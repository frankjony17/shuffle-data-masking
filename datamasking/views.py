import json
import math

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from datamasking.models import QueueProcess
from datamasking.service.producer import queue_publish_message, get_message
from introspection.models import Column, Database, Table
from introspection.views.introspection import get_connection
from processerror.models import ProcessError


class DataMaskingListView(generic.ListView):
    template_name = "datamasking/data_masking_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mask, table = self.get_configured_masks()
        database = self.get_database()
        errors = self.get_tables_with_errors()
        process_started, constraint_disabled = self.get_process_started()

        context['process_started'] = process_started
        context['constraint_disabled'] = constraint_disabled
        context['table_disabled'] = self.get_table_disabled(errors)
        context['tables_with_errors'] = errors
        context['configured_masks'] = mask
        context['configured_tables'] = table
        context['database'] = [database]

        return context

    def get_queryset(self):
        return self.get_table_count()

    def get_database(self):
        get_request = dict(self.request.GET)
        database = "Banco_de_dados"

        if len(get_request) > 0:
            return get_request["database"][0]

        return database

    def get_table_count(self):
        return Table.objects.filter(database__database_name=self.get_database()).count()

    def get_configured_masks(self):
        mask = Column.objects.filter(
            table__database__database_name=self.get_database()).filter(~Q(type_of_mask=0)).count()
        table = Table.objects.filter(Q(has_mask=True) & Q(database__database_name=self.get_database())).count()
        return mask, table

    def get_process_started(self):
        database = Database.objects.filter(database_name=self.get_database()).first()
        if database is None:
            return 0, 0
        return database.process_started, database.constraint_disabled

    @staticmethod
    def get_tables_with_errors():
        return ProcessError.objects.filter(error_type=1).count()

    def get_table_disabled(self, errors):
        table_count = self.get_table_count()
        if table_count > 0:
            return table_count - errors
        return 0


def disable_foreign_keys(request, database):
    queue_publish_message(get_message(db=database, table="DisableAllForeignKeys"))
    database_object = Database.objects.filter(database_name=database).first()
    database_object.process_started = True
    database_object.save()

    return HttpResponseRedirect(f"{reverse('datamasking:data-masking-list')}?database={database}")


def publish_message(request):
    payload = dict(request.POST)
    worker = int(payload.get('worker')[0])
    database_name = payload.get('database')[0]

    for table in Table.objects.filter(Q(database__database_name=database_name) & Q(has_mask=True)).all():
        count_rows = count_row_from_table(table.table_name, database_name)
        publish_to_queue(worker, count_rows, database_name, table.table_name, table.id)

    return HttpResponseRedirect(reverse('dashboard'))


def publish_to_queue(workers, count_rows, database_name, table_name, table_id):
    total = int(math.ceil(int(count_rows) / int(workers)))
    ended = 0
    workers += 1

    for _ in range(1, int(workers)):
        start, ended = get_parameters(ended, total)

        message = get_message(
            db=database_name, table=table_name, table_id=table_id, start=start, ended=ended, queue_process_id=0)
        message["Data"]["QueryProcessId"] = get_queue_process(message)
        queue_publish_message(message)


def count_row_from_table(table, database_name):
    db_connection = get_connection(database_name)

    with db_connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(1) FROM {table} WITH(NOLOCK)")
        count = cursor.fetchone()

    return count[0]


def get_parameters(ended, total):
    return int(ended), int(ended) + total


def get_queue_process(message, reduction_process=False):
    queue_process = QueueProcess()
    queue_process.table_id = message["Data"]["TableQueryId"]
    queue_process.processed_message = json.dumps(message)
    queue_process.reduction_process = reduction_process
    queue_process.save()
    return queue_process.id
