
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page

from datamasking.service.producer import queue_publish_message, get_message
from processerror import models


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProcessErrorListView(generic.ListView):
    template_name = "processerror/process_error.html"
    model = models.ProcessError
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        run_all, num_pages = 0, self.get_num_pages()
        run_error, status_error = self.get_error()

        if "run_all" in self.request.GET:
            run_all = num_pages

        context['run_error'] = run_error
        context['status_error'] = status_error
        context['run_all'] = run_all

        return context

    def get_error(self):
        request_get = dict(self.request.GET)

        if "error" in request_get:
            pk = request_get["error"][0]
            try:
                models.ProcessError.objects.get(pk=pk)
                return pk, True
            except models.ProcessError.DoesNotExist:
                return 0, False
        return 0, False

    @staticmethod
    def get_num_pages():
        return models.ProcessError.objects.count()


def error_run(request):
    post = dict(request.POST)
    process_error = models.ProcessError.objects.get(pk=post["pk"][0])

    queue_publish_message(get_message(
        db=process_error.table.database.database_name,
        table="RunErrorQuery",
        error_query=process_error.original_query,
        error_id=process_error.process_error_id,
        queue_process_id=process_error.queue_process_id))

    return HttpResponseRedirect(f"{reverse('processerror:error-list')}?error={post['pk'][0]}")


def error_run_all(request):
    process_error = models.ProcessError.objects.all()

    for error in process_error:
        queue_publish_message(get_message(
            db=error.table.database.database_name,
            table=error.table.table_name,
            table_id=error.table_id,
            error_query=error.original_query,
            error_id=error.process_error_id,
            queue_process_id=error.queue_process_id))

    return HttpResponseRedirect(f"{reverse('processerror:error-list')}?run_all=ok")
