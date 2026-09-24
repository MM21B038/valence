from django.contrib import admin
from .models import (
    AppTheme,
    Workspace,
    ServerStack,
    Component,
    Connection
)

# Register your models here.
admin.site.register(AppTheme)
admin.site.register(Workspace)
admin.site.register(ServerStack)
admin.site.register(Component)
admin.site.register(Connection)