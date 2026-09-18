from langchain_mcp_adapters.client import MultiServerMCPClient
from agent.services.config.server import Server, DuplicateValueError
from typing import List

class MCPClient:
    
    def __init__(
        self,
        servers: List[Server]
    ):
        self.servers = servers
        self.names = [server.name for server in servers]
        self.client = None

    def connect(self):
        servers = {}
        for server in self.servers:
            if server.name in servers:
                raise DuplicateValueError(f"server name {server.name} found twice")
            servers[server.name] = server.dump_json()

        self.client = MultiServerMCPClient(servers)

    def append(self, server: Server):
        if server.name in self.names:
            raise DuplicateValueError(f"server with name {server.name} already there")
        self.servers.append(server)
        self.names.append(server.name)
        return True

    async def get_tools(self):
        if self.client is None:
            self.connect()

        if isinstance(self.client, MultiServerMCPClient):
            return await self.client.get_tools()

        else:
            raise Exception("client is not a MultiServerMCPClient")