from asgiref.sync import sync_to_async
from typing import List
from agent.services import LLM, Agent
from agent.models import LLMConfig, MCPServerConfig
from agent.errors import GetAgentError
from .mcp import get_mcp_tools


async def get_agent(llm_config: LLMConfig, servers: List[MCPServerConfig]):
    try:
        llm = LLM.from_config(llm_config)

        return Agent(
            model=llm,
            tools=await get_mcp_tools(servers)
        )
    except Exception as e:
        raise GetAgentError(str(e))
