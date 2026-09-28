from rest_framework import serializers
from dnd.models import (
    AppTheme,
    ServerStack,
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

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

class WorkspaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['uuid', 'name', 'type']
