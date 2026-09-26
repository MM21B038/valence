from django.contrib import admin
from protocol.models import (
    SkillTag,
    AgentSkillModel,
    AgentInterfaceModel,
    AgentCardModel,
    AgentExecutorModel
)

# Register your models here.
admin.site.register(SkillTag)
admin.site.register(AgentSkillModel)
admin.site.register(AgentInterfaceModel)
admin.site.register(AgentCardModel)
admin.site.register(AgentExecutorModel)