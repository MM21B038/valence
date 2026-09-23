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

class MCPServerConfigListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCPServerConfig
        fields = [
            "uuid",
            "name",
            "transport"
        ]

class ToolHideRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolHideRuleModel
        fields = "__all__"

class CompressionPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompressionPrompt
        fields = "__all__"

class CompressionPromptListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompressionPrompt
        fields = "__all__"
        extra_kwargs = {
            "prompt": {
                "write_only": True
            }
        }

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = "__all__"

class PromptListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = "__all__"
        extra_kwargs = {
            "content": {
                "write_only": True
            }
        }

class SystemPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemPrompt
        fields = "__all__"

class SystemPromptListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemPrompt
        fields = "__all__"
        extra_kwargs = {
            "content": {
                "write_only": True
            }
        }

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class SkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        extra_kwargs = {
            "content": {
                "write_only": True
            }
        }

class ThreadConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadConfig
        fields = "__all__"

class ThreadConfigListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadConfig
        fields = [
            "uuid",
            "name",
        ]
