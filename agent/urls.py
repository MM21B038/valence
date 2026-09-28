from django.urls import path

from agent.views.llm_config import (
    LLMProviderOptionView,
    LLMConfigView,
    LLMConfigListCreateView,
    LLMChatView
)

from agent.views.internal_tool import (
    InternalToolListCreateView
)

from agent.views.mcp_server_config import (
    MCPServerTransportOptionView,
    MCPServerConfigView,
    MCPServerConfigListCreateView
)

from agent.views.tool_hide_rule import (
    ToolHideRuleView,
    ToolHideRuleListCreateView
)

from agent.views.compression_prompt import(
    CompressionPromptView,
    CompressionPromptListCreateView
)

from agent.views.prompt import (
    PromptView,
    PromptListCreateView
)

from agent.views.system_prompt import (
    SystemPromptView,
    SystemPromptListCreateView
)

from agent.views.skill import (
    SkillView,
    SkillListCreateView
)

from agent.views.thread_config import (
    ThreadConfigView,
    ThreadConfigListCreateView
)

urlpatterns = [
    path(
        "llm-provider/",
        LLMProviderOptionView.as_view(),
        name="llm-provider"
    ),
    
    path(
        "llm-config/<uuid:uuid>/",
        LLMConfigView.as_view(),
        name="llm-config",
    ),

    path(
        "llm-config/",
        LLMConfigListCreateView.as_view(),
        name="llm-config-list",
    ),

    path(
        "llm-chat/<uuid:uuid>/",
        LLMChatView.as_view(),
        name="llm-chat"
    ),

    path(
        "internal-tool/",
        InternalToolListCreateView.as_view(),
        name="internal-tool-list",
    ),

    path(
        "mcp-serve-transport-option/",
        MCPServerTransportOptionView.as_view(),
        name="mcp-serve-transport-option",
    ),

    path(
        "mcp-server-config/<uuid:uuid>/",
        MCPServerConfigView.as_view(),
        name="mcp-server-config",
    ),

    path(
        "mcp-server-config/",
        MCPServerConfigListCreateView.as_view(),
        name="mcp-server-config-list",
    ),

    path(
        "tool-hide-rule/<uuid:uuid>/",
        ToolHideRuleView.as_view(),
        name="tool-hide-rule",
    ),

    path(
        "tool-hide-rule/",
        ToolHideRuleListCreateView.as_view(),
        name="tool-hide-rule-list",
    ),

    path(
        "compression-prompt/<uuid:uuid>/",
        CompressionPromptView.as_view(),
        name="compression-prompt",
    ),

    path(
        "compression-prompt/",
        CompressionPromptListCreateView.as_view(),
        name="compression-prompt-list",
    ),

    path(
        "prompt/<uuid:uuid>/",
        PromptView.as_view(),
        name="prompt",
    ),

    path(
        "prompt/",
        PromptListCreateView.as_view(),
        name="prompt-list",
    ),

    path(
        "system-prompt/<uuid:uuid>/",
        SystemPromptView.as_view(),
        name="system-prompt",
    ),

    path(
        "system-prompt/",
        SystemPromptListCreateView.as_view(),
        name="system-prompt-list",
    ),

    path(
        "skill/<uuid:uuid>/",
        SkillView.as_view(),
        name="skill",
    ),

    path(
        "skill/",
        SkillListCreateView.as_view(),
        name="skill-list",
    ),

    path(
        "thread-config/<uuid:uuid>",
        ThreadConfigView.as_view(),
        name="thread-config",
    ),

    path(
        "thread-config/",
        ThreadConfigListCreateView.as_view(),
        name="thread-config-list",
    ),
]