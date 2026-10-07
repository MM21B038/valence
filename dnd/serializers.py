from django.db import transaction
from rest_framework import serializers
from dnd.agent_executor_template import seed_agent_executor_template
from dnd.enums import WorkspaceTypeChoices
from dnd.models import (
    AppTheme,
    ServerStack,
    AgentSkillStack,
    AgentInterfaceStack,
    Component,
    Connection,
    Workspace,
)

class AppThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppTheme
        fields = "__all__"
        
class ServerStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerStack
        fields = '__all__'

class AgentSkillStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSkillStack
        fields = '__all__'

class AgentInterfaceStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentInterfaceStack
        fields = '__all__'

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

class ConnectionDetailSerializer(serializers.ModelSerializer):
    source = ComponentSerializer(read_only=True)
    target = ComponentSerializer(read_only=True)

    class Meta:
        model = Connection
        fields = ['uuid', 'source', 'target']

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

    def create(self, validated_data):
        supplied_components = validated_data.get('components') or []
        supplied_connections = validated_data.get('connections') or []
        with transaction.atomic():
            workspace = super().create(validated_data)
            if (
                workspace.type == WorkspaceTypeChoices.AGENT_EXECUTOR
                and not supplied_components
                and not supplied_connections
            ):
                seed_agent_executor_template(workspace)
        return workspace

class WorkspaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['uuid', 'name', 'type']

class WorkspaceDetailSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True, read_only=True)
    connections = ConnectionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Workspace
        fields = [
            'uuid',
            'name',
            'type',
            'components',
            'connections',
            'created_at',
            'updated_at',
        ]
