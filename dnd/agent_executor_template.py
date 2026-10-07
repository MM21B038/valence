from dnd.enums import ComponentTypeChoices
from dnd.models import Component, Connection, Workspace

# Positions follow the existing agent-executor canvases (demo, demo2):
# card centered above the executor, interface and skill stacks flanking the card,
# llm and thread flanking the executor, server stack centered underneath.
_NODES = (
    (ComponentTypeChoices.AGENT_CARD, 537.0, -11.0),
    (ComponentTypeChoices.AGENT_INTERFACE_STACK, 300.0, 128.0),
    (ComponentTypeChoices.AGENT_SKILL_STACK, 820.0, 128.0),
    (ComponentTypeChoices.AGENT_EXECUTOR, 537.0, 203.0),
    (ComponentTypeChoices.LLM_CONFIG, 199.0, 369.0),
    (ComponentTypeChoices.THREAD_CONFIG, 874.0, 369.0),
    (ComponentTypeChoices.SERVER_STACK, 537.0, 448.0),
)

_EDGES = (
    (ComponentTypeChoices.AGENT_INTERFACE_STACK, ComponentTypeChoices.AGENT_CARD),
    (ComponentTypeChoices.AGENT_SKILL_STACK, ComponentTypeChoices.AGENT_CARD),
    (ComponentTypeChoices.AGENT_CARD, ComponentTypeChoices.AGENT_EXECUTOR),
    (ComponentTypeChoices.LLM_CONFIG, ComponentTypeChoices.AGENT_EXECUTOR),
    (ComponentTypeChoices.THREAD_CONFIG, ComponentTypeChoices.AGENT_EXECUTOR),
    (ComponentTypeChoices.SERVER_STACK, ComponentTypeChoices.AGENT_EXECUTOR),
)


def seed_agent_executor_template(workspace: Workspace) -> None:
    """Place an unconfigured agent-executor canvas and wire its default edges."""
    nodes = {}
    for component_type, position_x, position_y in _NODES:
        nodes[component_type] = Component.objects.create(
            type=component_type,
            position_x=position_x,
            position_y=position_y,
            component_uuid=None,
        )

    workspace.components.set(nodes.values())
    workspace.connections.set(
        Connection.objects.create(source=nodes[source], target=nodes[target])
        for source, target in _EDGES
    )
