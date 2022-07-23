import json
import uuid

from django.conf import settings
from django.utils.timezone import now
from pika import BasicProperties

from datamasking.service import channel


def queue_publish_message(message: dict):
    channel.basic_publish(exchange=settings.QUEUE_DATA_MASKING_EXCHANGE,
                          routing_key=settings.QUEUE_DATA_MASKING,
                          body=json.dumps(message),
                          properties=BasicProperties(content_type='text/plain', delivery_mode=2))


def get_message(db, table, table_id=0, start=0, ended=0, queue_process_id=0,
                error_query='', error_id=0, reduction_ids=None):
    message = {
        "Data": {
            'Database': db,
            'TableQuery': table,
            'TableQueryId': table_id,
            'StartQuery': start,
            'EndQuery': ended,
            'QueryProcessId': queue_process_id,
            'ErrorProcessQuery': error_query,
            'ErrorProcessId': error_id,
            'ReductionIds': reduction_ids if reduction_ids is not None else [],
            'MessageDate': str(now())
        },
        "CorrelationId": str(uuid.uuid4())
    }
    return message
