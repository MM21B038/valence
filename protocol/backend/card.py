import asyncio
from asgiref.sync import sync_to_async
from a2a.types import AgentCard, AgentSkill, AgentInterface, AgentCapabilities
from protocol.backend import get_agent_skill, get_agent_interface
from protocol.models import AgentCardModel
from protocol.errors import GetAgentCardError

async def get_agent_card(agent_card: AgentCardModel):
    try:
        interfaces_list, skills_list = await asyncio.gather(
            sync_to_async(lambda: list(agent_card.supported_interfaces.all()))(),
            sync_to_async(lambda: list(agent_card.skills.all()))()
        )

        supported_interfaces = []
        skills = []

        interface_results = await asyncio.gather(
            *(get_agent_interface(item) for item in interfaces_list)
        )
        supported_interfaces = [
            res for res in interface_results if isinstance(res, AgentInterface)
        ]

        if not supported_interfaces:
            return GetAgentCardError("No valid supported interface")

        skill_results = await asyncio.gather(
            *(get_agent_skill(item) for item in skills_list)
        )
        skills = [
            res for res in skill_results if isinstance(res, AgentSkill)
        ]

        return AgentCard(
            name=agent_card.name,
            description=agent_card.description,
            version=agent_card.version,
            supported_interfaces=supported_interfaces,
            capabilities=AgentCapabilities(
                streaming=agent_card.streaming,
                push_notifications=agent_card.push_notifications
            ),
            default_input_modes=["text/plain"],
            default_output_modes=["text/plain"],
            skills=skills,
        )
    except Exception as e:
        raise GetAgentCardError(str(e))