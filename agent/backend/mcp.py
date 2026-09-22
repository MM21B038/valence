from asgiref.sync import sync_to_async
from typing import List
from agent.services.config import Server, MCPClient
from agent.models import MCPServerConfig
from agent.errors import GetMCPToolsError, GetMCPPromptsError

async def get_server_tools(server: MCPServerConfig):
    try:
        servers = [Server.from_config(server)]
        client = MCPClient(servers)
        client.connect()
        return await client.get_tools()
    except Exception as e:
        raise GetMCPToolsError(str(e))

async def get_server_prompts(server: MCPServerConfig):
    try:
        servers = [Server.from_config(server)]
        client = MCPClient(servers)
        client.connect()
        return await client.get_prompt()
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

