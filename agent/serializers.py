from rest_framework import serializers
from agent.models import LLMConfig, InternalTool, MCPServerConfig

class LLMConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMConfig
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'created_at']

class LLMConfigListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMConfig
        fields = ['uuid', 'provider', 'model']

class InternalToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalTool
        fields = ['uuid', 'name', 'description']

class MCPServerConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMConfig
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'created_at']

class MCPServerConfigListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMConfig
        fields = ['uuid', 'name', 'transport']