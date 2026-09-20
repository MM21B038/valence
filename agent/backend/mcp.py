from asgiref.sync import sync_to_async
from typing import List
from agent.services.config import Server, MCPClient
from agent.models import MCPServerConfig
from agent.errors import GetMCPToolsError

# async def get_mcp_tools(server_uuids: List[str]):
#     servers = []
#     for uuid in server_uuids:
#         try:
#             server = MCPServerConfig.objects.get(uuid=uuid)
#             servers.append(Server.from_config(server))
#         except Exception as e:
#             return GetMCPToolsError(str(e))

#     try:
#         client = MCPClient(servers)
#         client.connect()
#         return await client.get_tools()
#     except Exception as e:
#         GetMCPToolsError(str(e))

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

