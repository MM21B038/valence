from rest_framework import serializers
from protocol.models import (
    SkillTag,
    AgentSkillModel,
    AgentInterfaceModel,
    AgentCardModel,
    AgentExecutorModel,
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

class AgentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentCardModel
        fields = '__all__'

class AgentCardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentCardModel
        fields = ['uuid', 'name', 'version']

class AgentExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentExecutorModel
        fields = '__all__'

class AgentExecutorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentExecutorModel
        fields = ['uuid', 'name', 'host', 'port', 'rpc_url']
        