import json

from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from datamasking.service.producer import get_message, queue_publish_message
from datamasking.views import get_queue_process
from introspection.models import Table, RelativeTable, Column


class ReductionListView(generic.ListView):
    template_name = "databasereduction/reduction_start_list.html"
    database = "Banco_de_dados"
    tables = []

    def get_queryset(self):
        if "database" in self.request.GET:
            self.database = self.request.GET.get("database")
            self.tables = Table.objects.filter(database__database_name=self.database)
        return self.tables

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'] = self.database
        return context


def reduction_get_relative_table(request):
    table_name = []
    relative_table = RelativeTable.objects.filter(principal_table_id=request.GET.get("pk")).all()

    for table in relative_table:
        table_name.append(table.secondary_table.table_name)

    column = Column.objects.filter(Q(table_id=request.GET.get("pk")) & Q(primary_key=True))

    return JsonResponse({
        "result": json.dumps(table_name),
        "total": len(table_name),
        "column_pk": [c.column_name for c in column]
    })


def reduction_start(request):
    table = Table.objects.get(pk=request.POST.get("table_id"))
    column_pk = Column.objects.filter(Q(table_id=table.id) & Q(primary_key=True))
    primary_key = []

    for column in column_pk:
        primary_key.append({
            "ColumnName": column.column_name,
            "PrimaryKeys": request.POST[column.column_name].split(',')
        })

    message = get_message(
        db=request.POST.get("database"),
        table=table.table_name,
        table_id=table.id,
        ended=request.POST.get("total-row"),
        reduction_ids=primary_key,
        queue_process_id=0)

    message["Data"]["QueryProcessId"] = get_queue_process(message, True)
    queue_publish_message(message)

    return HttpResponseRedirect(f"{reverse('dashboard')}?database={database}")



