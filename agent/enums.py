from django.db import models

class LLMProvider(models.TextChoices):
    OPENAI = "openai"
    OPENAI_COMPATIBLE = "openai-compatible"
    OPENROUTER = "openrouter"

class ServerTransport(models.TextChoices):
    STDIO = "stdio"
    HTTP = "http"