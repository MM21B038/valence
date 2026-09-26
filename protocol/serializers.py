from rest_framework import serializers
from protocol.models import (
    SkillTag,
    AgentSkillModel,
    AgentInterfaceModel,
)

class SkillTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTag
        fields = '__all__'

class AgentSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSkillModel
        fields = '__all__'

class AgentSkillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSkillModel
        fields = ['uuid', 'name', 'tags']

class AgentInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentInterfaceModel
        fields = '__all__'