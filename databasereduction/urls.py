from django.conf.urls import url
from django.urls import path

from databasereduction.views import ReductionListView, reduction_start, reduction_get_relative_table

app_name = "databasereduction"

urlpatterns = [
    url('reduction/list/', ReductionListView.as_view(), name="reduction-start"),

    path('reduction/start/', reduction_start, name="reduction-start-load"),

    path('reduction/get-relative-table/', reduction_get_relative_table, name="reduction-get-relative-table")
]
