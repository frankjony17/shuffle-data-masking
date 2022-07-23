
from django.db.models import Q, Sum
from django.views import generic

from datamasking.models import QueueProcess
from introspection.models import Column, Database, Table
from introspection.views.introspection import get_connection


class DashboardView(generic.ListView):
    template_name = "dashboard/dashboard.html"
    paginate_by = 10
    number_of_record = 0
    record_processed = 0
    number_of_tables = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        database_id = self.get_database_value("id")

        reduction_started = self.get_reduction_started()

        if reduction_started:
            reduction_count = self.get_reduction_count()
            reduction_total = self.get_reduction_total()
            context['reduction_started'] = self.get_reduction_started()
            context['number_of_tables'] = self.get_number_of_tables()
            context['reduction_total'] = reduction_total
            context['reduction_count'] = reduction_count
            context['reduction_percent'] = self.get_percent_finished(reduction_count, reduction_total)

        else:
            context['number_of_tables'] = self.number_of_tables
            context['configured_masks'] = self.get_configured_masks(database_id)
            context['processed_masks'] = self.get_processed_masks(database_id)
            context['number_of_record'] = self.number_of_record
            context['record_processed'] = self.record_processed

        return context

    def get_queryset(self):
        data_query = []
        table_objects = Table.objects.filter(
            Q(database_id=self.get_database_value("id")) & Q(has_mask=1)).all()
        database_name = self.get_database_value("database_name")

        if database_name == "EMPTY_DATABASE_NAME":
            return data_query
        db_connection = get_connection(database_name)

        with db_connection.cursor() as cursor:
            for table in table_objects:
                self.process_data(table, cursor, data_query)

        return data_query

    def process_data(self, table, cursor, data_query):
        start_date, local_record_processed = self.get_start_date_and_records_processed(table.id)
        local_number_of_record = self.get_number_of_records(cursor, table.table_name)

        data_query.append({
            "table": table.table_name,
            "start_date": start_date,
            "number_of_record": local_number_of_record,
            "record_processed": local_record_processed,
            "percent_finished": self.get_percent_finished(local_record_processed, local_number_of_record)
        })
        self.number_of_record += local_number_of_record
        self.record_processed += local_record_processed
        self.number_of_tables += 1

    @staticmethod
    def get_database_value(value):
        database = Database.objects.filter(Q(constraint_disabled=1) & Q(process_started=0)).first()
        if database:
            return database.database_name if value == "database_name" else database.id
        return "EMPTY_DATABASE_NAME" if value == "database_name" else 0

    @staticmethod
    def get_configured_masks(database_id):
        return Column.objects.filter(table__database_id=database_id).filter(~Q(type_of_mask=0)).count()

    @staticmethod
    def get_processed_masks(database_id):
        processed = QueueProcess.objects.filter(table__database_id=database_id).aggregate(Sum('processed_masking'))

        if processed['processed_masking__sum'] is None:
            processed['processed_masking__sum'] = 0

        return processed['processed_masking__sum']

    @staticmethod
    def get_percent_finished(record_processed, number_of_records):
        percent_finished = 0
        if record_processed > 0 and number_of_records > 0:
            percent_finished = round(100 * (record_processed / number_of_records), 2)
        return percent_finished

    @staticmethod
    def get_start_date_and_records_processed(table_id):
        try:
            start_process = QueueProcess.objects.filter(~Q(start_process=None)).earliest('start_process').start_process
            record_processed = QueueProcess.objects.filter(table_id=table_id).aggregate(Sum('processed_masking'))

            if record_processed['processed_masking__sum'] is None:
                record_processed['processed_masking__sum'] = 0

            return start_process, record_processed['processed_masking__sum']
        except QueueProcess.DoesNotExist:
            return None, 0

    @staticmethod
    def get_number_of_records(cursor, table):
        cursor.execute(f"SELECT COUNT(1) FROM {table} WITH(NOLOCK)")
        count = cursor.fetchone()
        return count[0]

    @staticmethod
    def get_reduction_started():
        count = Database.objects.filter(reduction_started=1).count()
        if count > 0:
            return True
        return False

    @staticmethod
    def get_number_of_tables():
        return Table.objects.filter(database__reduction_started=1).count()

    @staticmethod
    def get_reduction_total():
        return QueueProcess.objects.filter(reduction_process=1).count()

    @staticmethod
    def get_reduction_count():
        return QueueProcess.objects.filter(
            Q(reduction_process=1) & Q(ended_process__isnull=False)).count()
