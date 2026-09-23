from django.contrib import admin
from agent.models import (
    LLMConfig, 
    InternalTool, 
    MCPServerConfig, 
    ToolHideRuleModel,
    CompressionPrompt,
    Prompt,
    SystemPrompt,
    Skill,
    ThreadConfig,
)

# Register your models here.

admin.site.register(LLMConfig)
admin.site.register(InternalTool)
admin.site.register(MCPServerConfig)
admin.site.register(ToolHideRuleModel)
admin.site.register(CompressionPrompt)
admin.site.register(Prompt)
admin.site.register(SystemPrompt)
admin.site.register(Skill)
admin.site.register(ThreadConfig)