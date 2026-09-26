from django.urls import path
from protocol.views.agent_skill import AgentSkillView, AgentSkillListView
from protocol.views.skill_tag import SkillTagView
from protocol.views.agent_interface import AgentInterfaceView

urlpatterns = [

    path(
        'skill-tag/',
        SkillTagView.as_view(),
        name='skill-tag',
    ),

    path(
        'skill-tag/<uuid:uuid>/',
        SkillTagView.as_view(),
        name='skill-tag',
    ),


    path(
        'agent-skill/<uuid:uuid>/',
        AgentSkillView.as_view(),
        name='agent-skill',
    ),

    path(
        'agent-skill/',
        AgentSkillListView.as_view(),
        name='agent-skill-list',
    ),

    path(
        'agent-interface/',
        AgentInterfaceView.as_view(),
        name='agent-interface',
    ),

    path(
        'agent-interface/<uuid:uuid>/',
        AgentInterfaceView.as_view(),
        name='agent-interface-patch-delete',
    ),
]