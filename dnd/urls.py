from django.urls import path
from dnd.views.app_theme import AppThemeView


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
    
]