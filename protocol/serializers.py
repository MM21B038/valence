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


class AgentExecutorContainerSerializer(serializers.Serializer):
    uuid = serializers.CharField(allow_null=True, required=False)
    container_name = serializers.CharField(allow_null=True, required=False)
    status = serializers.CharField()
    image = serializers.CharField(allow_null=True, required=False)
    message = serializers.CharField(required=False)


class WorkspaceContainerSerializer(serializers.Serializer):
    network = serializers.CharField(allow_null=True, required=False)
    containers = AgentExecutorContainerSerializer(many=True)


class WorkspaceNetworkStatusSerializer(serializers.Serializer):
    name = serializers.CharField()
    exists = serializers.BooleanField()


class WorkspaceExecutorStatusSerializer(serializers.Serializer):
    agent_executor_uuid = serializers.CharField()
    name = serializers.CharField(allow_null=True)
    host = serializers.CharField(allow_null=True)
    port = serializers.IntegerField(allow_null=True)
    container_name = serializers.CharField(allow_null=True)
    container_status = serializers.CharField()
    image = serializers.CharField(allow_null=True)
    connected_to = serializers.ListField(
        child=serializers.CharField(),
        required=False,
    )


class WorkspaceStatusSerializer(serializers.Serializer):
    workspace_uuid = serializers.CharField()
    workspace_name = serializers.CharField()
    workspace_type = serializers.CharField()
    state = serializers.CharField()
    network = WorkspaceNetworkStatusSerializer(allow_null=True)
    executors = WorkspaceExecutorStatusSerializer(many=True)


class ProcessContainerSerializer(serializers.Serializer):
    agent_executor_uuid = serializers.CharField()
    name = serializers.CharField(allow_null=True)
    container_status = serializers.CharField()
    container_name = serializers.CharField(allow_null=True)
    port = serializers.IntegerField(allow_null=True)


class ProcessWorkspaceSerializer(serializers.Serializer):
    workspace_uuid = serializers.CharField()
    workspace_name = serializers.CharField()
    workspace_type = serializers.CharField()
    state = serializers.CharField()
    running_count = serializers.IntegerField()
    expected_count = serializers.IntegerField()
    containers = ProcessContainerSerializer(many=True)


class ProcessListSerializer(serializers.Serializer):
    processes = ProcessWorkspaceSerializer(many=True)
