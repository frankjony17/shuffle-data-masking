from django.conf.urls import url

from processerror.views import ProcessErrorListView, error_run, error_run_all

app_name = "processerror"

urlpatterns = [
    url("list/", ProcessErrorListView.as_view(), name="error-list"),
    url('error-run/', error_run, name="error-run"),
    url('error-run-all/', error_run_all, name="error-run-all"),
]
