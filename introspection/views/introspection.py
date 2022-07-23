import json

from django.contrib import messages
from django.db import connections
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.connection import ConnectionDoesNotExist, ConnectionProxy
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from introspection import forms, models


class IntrospectionListView(generic.ListView):
    form_class = forms.DatabaseChoice
    template_name = "introspection/introspection_update.html"
    paginate_by = 1
    database = "Banco_de_dados"
    kw = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['database'] = self.database
        context['kw'] = self.kw
        return context

    def get_queryset(self):
        payload = dict(self.request.GET)
        introspection = []

        if "database" not in payload:
            return introspection
        self.database = payload["database"][0]

        if "kw" in payload and payload["kw"][0] != "":
            self.kw = payload["kw"][0]
            tables = models.Table.objects.filter(
                Q(database__database_name=self.database) & Q(table_name__contains=self.kw))
        else:
            tables = models.Table.objects.filter(database__database_name=self.database)

        for table in tables:
            columns = models.Column.objects.filter(table=table.id).all()
            introspection.append({"table_id": table.id, "table_name": table.table_name, "columns": columns})

        return introspection


def introspection_update_data_mask(request):
    kw, count = "", 0
    request_get, request_post = dict(request.GET), dict(request.POST)
    database = request_get["database"][0]

    if "kw" in request_get:
        kw = request_get["kw"][0]

    for item in request_post["mask_type"]:
        if item != '0':
            mask = json.loads(item.strip("'").replace("\'", "\""))
            column = models.Column.objects.get(pk=mask["pk"])
            column.type_of_mask = mask["type"]
            column.save()
            count += 1

    if count > 0:
        table = models.Table.objects.filter(table_name=request_post["table_name"][0]).first()
        table.has_mask = True
        table.save()

    return HttpResponseRedirect(f'/introspection/list/?database={database}&page={request_post["page"][0]}&kw={kw}')


def remove_data_mask(request, pk, page):
    column = models.Column.objects.get(pk=pk)
    column.type_of_mask = 0
    column.save()

    mask_count = models.Column.objects.filter(
        Q(table__table_name=column.table.table_name) & ~Q(type_of_mask=0)).count()

    if mask_count == 0:
        table = models.Table.objects.get(pk=column.table.id)
        table.has_mask = 0
        table.save()

    kw = dict(request.GET)["kw"][0]
    return HttpResponseRedirect(
        f'/introspection/list/?database={column.table.database.database_name}&page={page}&kw={kw}')


def load_introspection(request):
    payload = dict(request.POST)
    database_name = payload.get('database')[0]
    connection = get_connection(database_name)
    try:
        database = get_or_create_database(database_name)
        table_names = connection.introspection.table_names()

        for table in table_names:
            table_obj = get_or_create_table(table, database)
            column_names = connection.introspection.get_table_description(
                connection.cursor(), table)
            get_or_create_table_column(table_obj, column_names)
        return HttpResponseRedirect(reverse('introspection:introspection-list'))

    except ConnectionDoesNotExist:
        messages.error(request, _(f"A conexão '{database_name}' não existe."))
        return HttpResponseRedirect(reverse('introspection:introspection-list'))


def get_connection(database):
    return ConnectionProxy(connections, database)


def get_or_create_database(database):
    obj, created = models.Database.objects.get_or_create(
        database_name=database)
    return obj


def get_or_create_table(table_name, database):
    obj, created = models.Table.objects.get_or_create(
        table_name=table_name, database=database)
    return obj


def get_or_create_table_column(table, column_names):
    for column in column_names:
        _, _ = models.Column.objects.get_or_create(
            table=table, column_name=column.name)
