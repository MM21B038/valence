from django.db import models
import uuid
from protocol.enums import TransportProtocolChoices
from agent.models import LLMConfig, MCPServerConfig, ThreadConfig, InternalTool, SystemPrompt, Skill


class SkillTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SkillExample(models.Model):
    content = models.TextField(max_length=500)
    
class AgentSkillModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(SkillTag, blank=True, related_name='agent_skills')
    examples = models.ManyToManyField(SkillExample, blank=True, related_name='agent_skills')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AgentInterfaceModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(blank=True, null=True)
    protocol_binding = models.CharField(max_length=100, choices=TransportProtocolChoices, default=TransportProtocolChoices.JSONRPC)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AgentCardModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    supported_interfaces = models.ManyToManyField(AgentInterfaceModel, blank=True, related_name='agent_cards')
    streaming = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)
    skills = models.ManyToManyField(AgentSkillModel, blank=True, related_name='skills')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AgentExecutorModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    host = models.CharField(max_length=20)
    port = models.IntegerField()
    rpc_url = models.CharField(max_length=100, blank=True, null=True)
    mcp_servers = models.ManyToManyField(MCPServerConfig, blank=True, related_name='agents')
    llm_config = models.ForeignKey(LLMConfig, on_delete=models.DO_NOTHING)
    thread_config = models.ForeignKey(ThreadConfig, on_delete=models.DO_NOTHING)
    excluded_internal_tools = models.ManyToManyField(InternalTool, blank = True)
    system_prompt = models.ForeignKey(SystemPrompt, on_delete=models.DO_NOTHING)
    skills = models.ManyToManyField(Skill, blank=True, related_name='agents')
    agent_card = models.ForeignKey(AgentCardModel, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    