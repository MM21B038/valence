import uuid
from django.db import models
from django.db.models import DO_NOTHING
from dnd.enums import WorkspaceTypeChoices, ComponentTypeChoices

# Create your models here.
class Workspace(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    type = models.TextField(max_length=30, choices=WorkspaceTypeChoices.choices, default=WorkspaceTypeChoices.A2A)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Component(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.TextField(max_length=30, choices=ComponentTypeChoices.choices, default=ComponentTypeChoices.AGENT_EXECUTOR)
    position_x = models.FloatField(default=0.0)
    position_y = models.FloatField(default=0.0)
    component_uuid = models.UUIDField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} - {self.component_uuid}"

class Connection(models.Model):
    source = models.ForeignKey(Component, on_delete=DO_NOTHING)
    target = models.ForeignKey(Component, on_delete=DO_NOTHING)




