from rest_framework import serializers
from dnd.models import (
    AppTheme,
)

class AppThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppTheme
        fields = "__all__"
        
