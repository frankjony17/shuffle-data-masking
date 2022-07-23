
from django.urls import re_path, include, path
from django.conf import settings
from django.conf.urls.static import static

from dashboard.views import DashboardView
from datamasking import urls as data_masking_urls
from introspection.urls import introspection as introspection_urls
from introspection.urls import relationships as relationships_urls
from databasereduction import urls as database_reduction_urls
from processerror import urls as process_error_urls
from main.views import healthcheck, enable_constraints, EnableContraintsView

urlpatterns = [
    path('healthcheck/', healthcheck, name="healthcheck"),
    re_path(r'^$', DashboardView.as_view(), name="dashboard"),

    path('constraints/start/', EnableContraintsView.as_view(), name="constraints-enable"),
    path('constraints/enable/<str:database>/', enable_constraints, name="constraints-enable-start"),

    # introspection
    re_path(
        r'^introspection/',
        include(introspection_urls), name="introspection"),

    # database-reduction
    re_path(
        r'^databasereduction/',
        include(database_reduction_urls), name="databasereduction"),

    # relationships
    re_path(
      r'^relationships/',
      include(relationships_urls), name="relationships"),

    # data masking
    re_path(
        r'^datamasking/',
        include(data_masking_urls), name="introspection"),

    # process error
    re_path(
        r'^processerror/',
        include(process_error_urls), name="processerror"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
