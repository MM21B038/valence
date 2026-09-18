from django.db import models

class TransportProtocolChoices(models.TextChoices):
    HTTP_JSON = "http+json"
    JSONRPC = "jsonrpc"
    GRPC = "grpc"