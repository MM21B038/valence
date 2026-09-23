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

async def get_server_prompts(server: MCPServerConfig):
    server_name = server.name
    try:
        servers = [Server.from_config(server)]
        client = MCPClient(servers)
        client.connect()
        prompts = await client.list_prompts(server_name) or []

        result = []
        for prompt in prompts:
            prompt_messages = await client.get_prompt(
                server_name,
                prompt.name,
            )
            for message in prompt_messages or []:
                result.append(
                    ServerPrompt(
                        name=prompt.name,
                        prompt=str(message.content)
                    )
                )
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

