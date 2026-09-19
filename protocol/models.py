from django.db import models
from protocol.enums import TransportProtocolChoices
from agent.models import ServerConfig


class SkillTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SkillExample(models.Model):
    text = models.TextField(max_length=500)
    
class AgentSkillModel(models.Model):
    skill_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(SkillTag, blank=True, related_name='tags')
    examples = models.ManyToManyField(SkillExample, blank=True, related_name='examples')

    def __str__(self):
        return self.name

class AgentInterfaceModel(models.Model):
    url = models.URLField(blank=True, null=True)
    protocol_binding = models.CharField(max_length=100, choices=TransportProtocolChoices, default=TransportProtocolChoices.JSONRPC)

class AgentCardModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    supported_interfaces = models.ManyToManyField(AgentInterfaceModel, blank=True, related_name='supported_interfaces')
    streaming = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)
    skills = models.ManyToManyField(AgentSkillModel, blank=True, related_name='skills')

    def __str__(self):
        return self.name

class AgentModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip = models.CharField(max_length=20)
    port = models.IntegerField()
    servers = models.ManyToManyField(ServerConfig, blank=True, related_name='servers')
    system = models.TextField(blank=True)
    agent_card = models.ForeignKey(AgentCardModel, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.name
    