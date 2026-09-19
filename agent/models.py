import uuid
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField
from agent.enums import (
    LLMProvider,
    ServerTransport
)

class LLMConfig(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=100, choices=LLMProvider.choices, default=LLMProvider.OPENAI_COMPATIBLE)
    model = models.CharField(max_length=100)
    base_url = models.URLField(blank=True, null=True)
    api_key = EncryptedCharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class InternalTool(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)


class MCPServerConfig(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    transport = models.CharField(max_length=10, choices=ServerTransport.choices, default=ServerTransport.HTTP)
    url = models.URLField(blank=True, null=True)
    command = models.CharField(max_length=200, blank=True, null=True)
    args = models.JSONField(blank=True, null=True)
    env = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

class ToolHideRuleModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    server = models.ForeignKey(MCPServerConfig, on_delete=models.CASCADE)

class ThreadConfig(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tool_hide_rules = models.ManyToManyField(ToolHideRuleModel, blank = True)
    auto_hide_rule = models.BooleanField(default = False)
    token_limit = models.IntegerField(blank = True, null = True)
    per_tool_token_limit = models.IntegerField(blank = True, null = True)


class Skill(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    skill = models.TextField()