import uuid
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField
from .enums import LLMProvider, ServerTransport

class LLMConfig(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=100, choices=LLMProvider.choices, default=LLMProvider.OPENAI_COMPATIBLE)
    model = models.CharField(max_length=100)
    base_url = models.URLField(blank=True, null=True)
    api_key = EncryptedCharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.provider

class InternalTool(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MCPServerConfig(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    transport = models.CharField(max_length=10, choices=ServerTransport.choices, default=ServerTransport.HTTP)
    url = models.URLField(blank=True, null=True)
    command = models.CharField(max_length=200, blank=True, null=True)
    args = models.JSONField(blank=True, null=True)
    env = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ToolHideRuleModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    server = models.ForeignKey(MCPServerConfig, on_delete=models.CASCADE)

class CompressionPrompt(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, blank=True, null=True)
    prompt = models.TextField(max_length=1_000, blank = True, null = True)

class Prompt(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, blank=True, null=True)
    content = models.TextField(max_length=1_000)

class SystemPrompt(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, blank=True, null=True)
    content = models.TextField(max_length=1_000)

class ThreadConfig(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system_prompt = models.ForeignKey(SystemPrompt, on_delete=models.DO_NOTHING)
    compression_prompt = models.ForeignKey(CompressionPrompt, on_delete=models.DO_NOTHING)
    compression_token_limit = models.IntegerField(blank = True, null = True)
    tool_hide_rules = models.ManyToManyField(ToolHideRuleModel, blank = True, related_name="thread_configs")
    auto_hide_rule = models.BooleanField(default = False)
    token_limit = models.IntegerField(blank = True, null = True)
    per_tool_token_limit = models.IntegerField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Skill(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name