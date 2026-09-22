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

from agent.views.tool_hide_rule import (
    ToolHideRuleView,
    ToolHideRuleListView
)

from agent.views.compression_prompt import(
    CompressionPromptView,
    CompressionPromptListView
)

from agent.views.prompt import (
    PromptView,
    PromptListView
)

from agent.views.system_prompt import (
    SystemPromptView,
    SystemPromptListView
)

from agent.views.skill import (
    SkillView,
    SkillListView
)

from agent.views.thread_config import (
    ThreadConfigView,
    ThreadConfigListView
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
        "mcp-server-config/",
        MCPServerConfigListView.as_view(),
        name="mcp-server-config-list",
    ),

    path(
        "tool-hide-rule/<uuid:uuid>/",
        ToolHideRuleView.as_view(),
        name="tool-hide-rule",
    ),

    path(
        "tool-hide-rule/",
        ToolHideRuleListView.as_view(),
        name="tool-hide-rule-list",
    ),

    path(
        "compression-prompt/<uuid:uuid>/",
        CompressionPromptView.as_view(),
        name="compression-prompt",
    ),

    path(
        "compression-prompt/",
        CompressionPromptListView.as_view(),
        name="compression-prompt-list",
    ),

    path(
        "prompt/<uuid:uuid>/",
        PromptView.as_view(),
        name="prompt",
    ),

    path(
        "prompt/",
        PromptListView.as_view(),
        name="prompt-list",
    ),

    path(
        "system-prompt/<uuid:uuid>/",
        SystemPromptView.as_view(),
        name="system-prompt",
    ),

    path(
        "system-prompt/",
        SystemPromptListView.as_view(),
        name="system-prompt-list",
    ),

    path(
        "skill/<uuid:uuid>/",
        SkillView.as_view(),
        name="skill",
    ),

    path(
        "skill/",
        SkillListView.as_view(),
        name="skill-list",
    ),

    path(
        "thread-config/<uuid:uuid>",
        ThreadConfigView.as_view(),
        name="thread-config",
    ),

    path(
        "thread-config-list/",
        ThreadConfigListView.as_view(),
        name="thread-config-list",
    )
]