import pika
from django.conf import settings
from django.http import JsonResponse
from pika.exceptions import AMQPConnectionError

try:
    credentials = pika.PlainCredentials(settings.QUEUE_DATA_MASKING_USER, settings.QUEUE_DATA_MASKING_PASSWORD)
    parameters = pika.ConnectionParameters(
        settings.QUEUE_DATA_MASKING_HOST, settings.QUEUE_DATA_MASKING_PORT, virtual_host='/', credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(
        queue=settings.QUEUE_DATA_MASKING, durable=True, auto_delete=False, arguments={"x-queue-mode": "lazy"})
    channel.confirm_delivery()
except AMQPConnectionError:
    raise JsonResponse({'message': "CONNECTION ERROR: THE SERVER MQ IS DOWN"}, status=503)
