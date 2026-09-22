from rest_framework import serializers
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

class LLMConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMConfig
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'created_at']
        extra_kwargs = {
            "api_key": {
                "write_only": True
            }
        }

class InternalToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalTool
        fields = ['uuid', 'name', 'description']

class MCPServerConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCPServerConfig
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'created_at']

class MCPServerConfigListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCPServerConfig
        fields = "__all__"

class ToolHideRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolHideRuleModel
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'server', 'name', 'created_at']

class ToolHideRuleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolHideRuleModel
        fields = ['uuid', 'server', 'name']

class CompressionPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompressionPrompt
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'created_at']

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'created_at', 'server']

class SystemPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemPrompt
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'created_at']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'created_at']

class ThreadConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadConfig
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'created_at']

