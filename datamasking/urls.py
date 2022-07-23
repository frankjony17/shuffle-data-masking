from django.conf.urls import url
from django.urls import path

from datamasking.views import (DataMaskingListView, disable_foreign_keys,
                               publish_message)

app_name = "datamasking"

urlpatterns = [
    url('load-start/', DataMaskingListView.as_view(), name="data-masking-list"),
    url('publish-message/', publish_message, name="data-masking-publish-message"),
    path('disable/foreignkeys/<str:database>', disable_foreign_keys, name="data-masking-disable-foreign-keys"),
]
