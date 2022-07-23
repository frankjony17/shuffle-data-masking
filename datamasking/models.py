
from django.db import models

from introspection.models import Table


class QueueProcess(models.Model):
    start_process = models.DateTimeField(blank=True, null=True)
    ended_process = models.DateTimeField(blank=True, null=True)
    processed_masking = models.IntegerField(default=0)
    processed_message = models.TextField(blank=True, null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reduction_process = models.BooleanField(default=False)
