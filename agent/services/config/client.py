from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import List, Optional, Dict, Any, Union
from agent.services.config.server import Server, DuplicateValueError


class MCPClient:
    client: Optional[MultiServerMCPClient]
    
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
                return DuplicateValueError(f"server name {server.name} found twice")
            servers[server.name] = server.dump_json()

        self.client = MultiServerMCPClient(servers)

    def append(self, server: Server):
        if server.name in self.names:
            return DuplicateValueError(f"server with name {server.name} already there")
        self.servers.append(server)
        return True

    def _ensure_connected(self):
        if self.client is None:
            self.connect()

    async def get_tools(self):
        self._ensure_connected()

        if self.client is None:
            return
        
        return await self.client.get_tools()
        

    async def list_prompts(self, server_name: str):
        self._ensure_connected()

        if self.client is None:
            return

        async with self.client.session(server_name) as session:
            result = await session.list_prompts()

        return result

    async def list_resources(self, server_name: str):
        self._ensure_connected()

        if self.client is None:
            return

        async with self.client.session(server_name) as session:
            result = await session.list_resources()

        return result

    async def get_prompt(
        self,
        server_name: str,
        prompt_name: str,
        arguments: Optional[Dict[str, Any]] = None
    ):
        self._ensure_connected()

        if self.client is None:
            return

        return await self.client.get_prompt(
            server_name=server_name,
            prompt_name=prompt_name,
            arguments=arguments
        )

    async def get_resources(
        self,
        server_name: Optional[str] = None,
        uris: Optional[Union[str, List[str]]] = None
    ):
        self._ensure_connected()

        if self.client is None:
            return

        return await self.client.get_resources(
            server_name=server_name,
            uris=uris
        )