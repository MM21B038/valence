from django.db import models

class WorkspaceTypeChoices(models.TextChoices):
    AGENT_EXECUTOR = 'agent-executor'
    A2A = 'a2a'

class ComponentTypeChoices(models.TextChoices):
    MCP_SERVER = 'mcp-server'
    LLM_CONFIG = 'llm-config'
    THREAD_CONFIG = 'thread-config'
    AGENT_SKILL = 'agent-skill'
    AGENT_INTERFACE = 'agent-interface'
    AGENT_CARD = 'agent-card'
    AGENT_EXECUTOR = 'agent-executor'
    SERVER_STACK = 'server-stack'