from django.conf.urls import url
from django.urls import path

from introspection.views.relationships import (RelationsIntrospectionListView,
                                               relations_introspection_load,
                                               relations_introspection_remove, relations_introspection_add,
                                               relations_get_columns_by_table)

app_name = "relationships"

urlpatterns = [
    url('constraint/list/',
        RelationsIntrospectionListView.as_view(),
        name="constraint-list"),

    path('load/',
         relations_introspection_load,
         name="constraint-load"),

    path('constraint/add/',
         relations_introspection_add,
         name="constraint-add"),

    path('constraint/remove/<int:pk>/<str:key>/<str:page>/',
         relations_introspection_remove,
         name="constraint-remove"),

    path('constraint/get/columns/',
         relations_get_columns_by_table,
         name="get-columns-by-table")
]
