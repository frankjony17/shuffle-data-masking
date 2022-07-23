
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from datamasking.service.producer import queue_publish_message, get_message
from introspection.models import Database, Table
from processerror.models import ProcessError


def healthcheck(request):
    return HttpResponse("Up", content_type="text/plain")


class EnableContraintsView(generic.ListView):
    template_name = "contraints/enable_contraints.html"
    database = "Banco_de_dados"
    table_count = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        errors = self.get_tables_with_errors()

        context['database'] = self.database
        context['table_enabled'] = self.get_table_enabled(errors)
        context['tables_with_errors'] = errors
        context['is_database_enabled'] = self.is_database_enabled()

        return context

    def get_queryset(self):
        if "database" in self.request.GET:
            self.database = self.request.GET.get("database")
            self.table_count = Table.objects.filter(database__database_name=self.database).count()

        return self.table_count

    @staticmethod
    def get_tables_with_errors():
        return ProcessError.objects.filter(error_type=3).count()

    def get_table_enabled(self, errors):
        if self.table_count > 0:
            return self.table_count - errors
        return 0

    def is_database_enabled(self):
        database = None

        if "database" in self.request.GET:
            database = Database.objects.filter(database_name=self.request.GET.get("database")).first()
        if database is None:
            return False

        return database.constraint_disabled


def enable_constraints(request, database):
    queue_publish_message(get_message(db=database, table="EnableAllForeignKeys"))
    database_object = Database.objects.filter(database_name=database).first()
    database_object.process_started = False
    database_object.save()

    return HttpResponseRedirect(f"/constraints/start/?database={database}")
