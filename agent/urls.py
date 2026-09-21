from django.urls import path

from agent.views.llm_config import (
    LLMConfigView,
    LLMConfigListView
)

from agent.views.internal_tool import (
    InternalToolListView
)

from agent.views.mcp_server_config import (
    MCPServerConfigView,
    MCPServerConfigListView
)

urlpatterns = [
    path(
        "llm-config/<uuid:uuid>/",
        LLMConfigView.as_view(),
        name="llm-config",
    ),

    path(
        "llm-config/",
        LLMConfigListView.as_view(),
        name="llm-config-list",
    ),

    path(
        "internal-tool/",
        InternalToolListView.as_view(),
        name="internal-tool-list",
    ),

    path(
        "mcp-server-config/<uuid:uuid>/",
        MCPServerConfigView.as_view(),
        name="mcp-server-config",
    ),

    path(
        "llm-config/",
        MCPServerConfigListView.as_view(),
        name="mcp-server-config-list",
    ),
]