import json

from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic

from introspection.models import Table, Column, RelativeTable
from introspection.views import get_relations_query, get_primary_keys_query
from introspection.views.introspection import get_connection


class RelationsIntrospectionListView(generic.ListView):
    template_name = "relationships/relationships_update_list.html"
    paginate_by = 1
    database = "Banco_de_dados"
    kw = ""
    tables = None

    def get_queryset(self):
        relationships = []
        if "database" not in self.request.GET:
            return relationships

        table_qs = Table.objects.filter(database__database_name=self.request.GET.get("database"))
        self.tables = table_qs

        if "kw" in self.request.GET and self.request.GET.get("kw") != "":
            table_qs = table_qs.filter(table_name__contains=self.request.GET.get("kw"))

        for table in table_qs:
            relationships.append({
                "table_id": table.id,
                "table_name": table.table_name,
                "table_columns": Column.objects.filter(Q(table=table.id)),
                "relative_table": RelativeTable.objects.filter(secondary_table_id=table.id)
            })
        return relationships

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "kw" in self.request.GET and self.request.GET.get("kw") != "":
            context['kw'] = self.request.GET.get("kw")
        if "database" in self.request.GET:
            context['database'] = self.request.GET.get("database")
        context['tables'] = self.tables
        return context


def relations_introspection_load(request):
    connection = get_connection(request.POST.get('database'))

    with connection.cursor() as cursor:
        for table in Table.objects.filter(database__database_name=request.POST.get('database')):
            # Update or create relationships.
            update_or_create_relationships(
                cursor=cursor, table=table, database=request.POST.get('database'))
            # Update primary_key for table.
            update_primary_key_for_table(cursor=cursor, table=table)

    return HttpResponseRedirect(f"relationships/constraint/list/?database={request.POST.get('database')}")


def update_or_create_relationships(cursor, table, database):
    cursor.execute(get_relations_query(table.table_name))
    # REFERENCED_TABLE_NAME = relations[0],
    # REFERENCING_COLUMN_NAME = relations[1],
    # REFERENCED_COLUMN_NAME = relations[2]
    try:
        for relations in cursor.fetchall():
            _, _ = RelativeTable.objects.update_or_create(
                principal_table=get_table_by_name(relations[0], database),
                principal_column_name=get_column_by_name(relations[0], column_name=relations[2]),
                secondary_table_id=table.id,
                secondary_column_name=get_column_by_name(table.table_name, column_name=relations[1])
            )
    except IntegrityError as err:
        print(err)
    except Exception as exc:
        print(exc)


def relations_introspection_add(request):
    if "btn_fk" in request.POST:
        relative_table = RelativeTable()
        relative_table.principal_table_id = request.POST.get("principal_table")
        relative_table.principal_column_name_id = request.POST.get("principal_column")
        relative_table.secondary_table_id = request.POST.get("secondary_table")
        relative_table.secondary_column_name_id = request.POST.get("secondary_column")
        relative_table.save()
    else:
        column = Column.objects.get(pk=request.POST.get("secondary_column"))
        column.primary_key = True
        column.save()

    return HttpResponseRedirect("relationships/constraint/list/"
                                f"?database={request.GET.get('database')}"
                                f"&kw={request.GET.get('kw')}"
                                f"&page={request.GET.get('page')}")


def relations_introspection_remove(request, pk, key, page):
    if key == "FK":
        relative_table = RelativeTable.objects.get(pk=pk)
        relative_table.delete()
    elif key == "PK":
        column = Column.objects.get(pk=pk)
        column.primary_key = False
        column.save()
    else:
        columns = Column.objects.filter(table_id=pk)
        for column in columns:
            column.primary_key = False
            column.save()

    return HttpResponseRedirect("relationships/constraint/list/"
                                f"?database={request.GET.get('database')}"
                                f"&kw={request.GET.get('kw')}"
                                f"&page={page}")


def relations_get_columns_by_table(request):
    columns = Column.objects.filter(table_id=request.GET.get("pk"))
    return JsonResponse({"result": json.dumps(list(columns.values('id', 'column_name')))})


def update_primary_key_for_table(cursor, table):
    cursor.execute(get_primary_keys_query(table.table_name))
    # COLUMN_NAME = column_pk[0]
    for column_pk in cursor.fetchall():
        column = get_column_by_name(table.table_name, column_name=column_pk[0])
        column.primary_key = True
        column.save()


def get_table_by_name(table_name, database_name):
    return Table.objects.filter(
        Q(table_name=table_name) & Q(database__database_name=database_name)).first()


def get_column_by_name(table_name, column_name):
    return Column.objects.filter(Q(table__table_name=table_name) & Q(column_name=column_name)).first()
