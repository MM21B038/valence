import uuid
from django.db import models
from colorfield.fields import ColorField
from dnd.enums import WorkspaceTypeChoices, ComponentTypeChoices
from agent.models import MCPServerConfig

class AppTheme(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    deep = ColorField(default="#202121")
    mid = ColorField(default="#3D4242")
    accent = ColorField(default="#8A8D8D")
    sand = ColorField(default="#B5AF99")
    default = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class Workspace(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    type = models.TextField(max_length=30, choices=WorkspaceTypeChoices.choices, default=WorkspaceTypeChoices.A2A)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ServerStack(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    servers = models.ManyToManyField(MCPServerConfig, blank=True, related_name='stack')

class Component(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.TextField(max_length=30, choices=ComponentTypeChoices.choices, default=ComponentTypeChoices.AGENT_EXECUTOR)
    position_x = models.FloatField(default=0.0)
    position_y = models.FloatField(default=0.0)
    color_code = ColorField(default="#47B9B9")
    component_uuid = models.UUIDField()
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.workspace.name} - {self.type}"

class Connection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(Component, on_delete=models.DO_NOTHING, related_name="outgoing")
    target = models.ForeignKey(Component, on_delete=models.DO_NOTHING, related_name="incoming")

    




