from rest_framework import serializers
from agent.models import LLMConfig

class LLMConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMConfig
        fields = "__all__"
        read_only_fields = ['id', 'uuid', 'created_at']
