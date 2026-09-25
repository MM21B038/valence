from asgiref.sync import sync_to_async
from typing import List
from pydantic import BaseModel
from agent.services.config import Server, MCPClient
from agent.models import MCPServerConfig
from agent.errors import GetMCPToolsError, GetMCPPromptsError

class ServerPrompt(BaseModel):
    name: str
    prompt: str

async def get_server_tools(server: MCPServerConfig):
    try:
        servers = [Server.from_config(server)]
        client = MCPClient(servers)
        client.connect()
        return await client.get_tools()
    except Exception as e:
        raise GetMCPToolsError(str(e))

def _format_prompt_messages(messages) -> str:
    parts = []
    for message in messages:
        content = message.content
        if isinstance(content, str):
            parts.append(content)
        else:
            parts.append(str(content))
    return "\n\n".join(parts)


async def get_server_prompts(server: MCPServerConfig) -> list[tuple[str, str]]:
    try:
        servers = [Server.from_config(server)]
        client = MCPClient(servers)
        client.connect()
        prompt_list = await client.list_prompts(server.name)
        if not prompt_list:
            return []

        prompts: list[tuple[str, str]] = []
        for prompt_meta in prompt_list:
            messages = await client.get_prompt(server.name, prompt_meta.name)
            if not messages:
                continue
            prompts.append((prompt_meta.name, _format_prompt_messages(messages)))
        return prompts
    except Exception as e:
        raise GetMCPPromptsError(str(e))

async def get_mcp_tools(server_list: List[MCPServerConfig]):
    servers = []
    try:
        for server in server_list:
            servers.append(Server.from_config(server))
        client = MCPClient(servers)
        client.connect()
        return await client.get_tools()
    except Exception as e:
        raise GetMCPToolsError(str(e))

async def get_mcp_tools_by_id(server_list: List[str]):
    servers = []
    try:
        for server in set(server_list):
            config = await sync_to_async(
                MCPServerConfig.objects.get
            )(uuid=server)
            servers.append(Server.from_config(config))
        client = MCPClient(servers)
        client.connect()
        return await client.get_tools()
    except Exception as e:
        raise GetMCPToolsError(str(e))

