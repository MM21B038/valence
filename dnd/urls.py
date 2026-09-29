from django.urls import path
from dnd.views.app_theme import AppThemeView
from dnd.views.server_stack import ServerStackView
from dnd.views.agent_skill_stack import AgentSkillStackView
from dnd.views.agent_interface_stack import AgentInterfaceStackView
from dnd.views.component import ComponentView
from dnd.views.connection import ConnectionView
from dnd.views.workspace import WorkspaceView, WorkspaceListCreateView


urlpatterns = [

    path(
        'app-theme/',
        AppThemeView.as_view(),
        name='app-theme',
    ),

    path(
        'app-theme/<uuid:uuid>/',
        AppThemeView.as_view(),
        name='app-theme-path-delete',
    ),
    
    path(
        'server-stack/<uuid:uuid>/',
        ServerStackView.as_view(),
        name='server-stack',
    ),

    path(
        'server-stack/',
        ServerStackView.as_view(),
        name='server-stack-create',
    ),

    path(
        'agent-skill-stack/<uuid:uuid>/',
        AgentSkillStackView.as_view(),
        name='agent-skill-stack',
    ),

    path(
        'agent-skill-stack/',
        AgentSkillStackView.as_view(),
        name='agent-skill-stack-create',
    ),

    path(
        'agent-interface-stack/<uuid:uuid>/',
        AgentInterfaceStackView.as_view(),
        name='agent-interface-stack',
    ),

    path(
        'agent-interface-stack/',
        AgentInterfaceStackView.as_view(),
        name='agent-interface-stack-create',
    ),

    path(
        'component/<uuid:uuid>/',
        ComponentView.as_view(),
        name='component',
    ),

    path(
        'component/',
        ComponentView.as_view(),
        name='component-create',
    ),

    path(
        'connection/<uuid:uuid>/',
        ConnectionView.as_view(),
        name='connection',
    ),

    path(
        'connection/',
        ConnectionView.as_view(),
        name='connection-create',
    ),

    path(
        'workspace/<uuid:uuid>/',
        WorkspaceView.as_view(),
        name='workspace',
    ),

    path(
        'workspace/',
        WorkspaceListCreateView.as_view(),
        name='workspace-list-create',
    ),
]