from django.urls import path
from dnd.views.app_theme import AppThemeView
from dnd.views.workspace import WorkspaceView, WorkspaceListCreateView
from dnd.views.server_stack import ServerStackView


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
        'workspace/<uuid:uuid>/',
        WorkspaceView.as_view(),
        name='workspace',
    ),

    path(
        'workspace/',
        WorkspaceListCreateView.as_view(),
        name='workspace-list-create',
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
]