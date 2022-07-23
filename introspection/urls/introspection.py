from django.conf.urls import url
from django.urls import path

from introspection.views.introspection import (IntrospectionListView,
                                               introspection_update_data_mask,
                                               load_introspection,
                                               remove_data_mask)

app_name = "introspection"

urlpatterns = [
    url('list/', IntrospectionListView.as_view(), name="introspection-list"),
    path('load/', load_introspection, name="introspection-load"),
    path('mask-remove/<int:pk>/<str:page>/', remove_data_mask, name="introspection-remove-mask"),
    path('update-data-mask/', introspection_update_data_mask, name="introspection-update-data-mask")
]
