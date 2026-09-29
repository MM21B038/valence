from asgiref.sync import sync_to_async
from a2a.types import AgentInterface
from a2a.utils import TransportProtocol
from protocol.models import AgentInterfaceModel
from protocol.errors import GetAgentInterfaceError

async def get_agent_interface(agent_interface: AgentInterfaceModel):
    try:
        return AgentInterface(
            url=f"http://{agent_interface.host}:{agent_interface.port}",
            protocol_binding=TransportProtocol(agent_interface.protocol_binding)
        )
    except Exception as e:
        raise GetAgentInterfaceError(str(e))
