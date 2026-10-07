from django.urls import path
from protocol.views.agent_skill import AgentSkillView, AgentSkillListCreateView
from protocol.views.skill_tag import SkillTagView
from protocol.views.agent_interface import AgentInterfaceView
from protocol.views.agent_card import AgentCardView, AgentCardListCreateView
from protocol.views.agent_executor import AgentExecutorView, AgentExecutorListCreateView
from protocol.views.agent_executor_lifecycle import AgentExecutorImageBuildView

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
        AgentSkillListCreateView.as_view(),
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

    path(
        'agent-card/<uuid:uuid>/',
        AgentCardView.as_view(),
        name='agent-card',
    ),

    path(
        'agent-card/',
        AgentCardListCreateView.as_view(),
        name='agent-card-list',
    ),

    path(
        'agent-executor/image/build/',
        AgentExecutorImageBuildView.as_view(),
        name='agent-executor-image-build',
    ),

    path(
        'agent-executor/<uuid:uuid>/',
        AgentExecutorView.as_view(),
        name='agent-executor',
    ),

    path(
        'agent-executor/',
        AgentExecutorListCreateView.as_view(),
        name='agent-executor-list',
    ),
]
