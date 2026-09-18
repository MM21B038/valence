from typing import Any, Dict, List, Optional
from agent.enums import ServerTransport

class Server:
    
    def __init__(
        self,
        name: str,
        transport: ServerTransport = ServerTransport.HTTP,
        url: Optional[str] = None,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, Any]] = None
    ):
        
        self.name = name
        self.transport = transport
        self.url = url
        self.command = command
        self.args = args
        self.env = env

    def dump_json(self):
        config = {}
        config["transport"] = self.transport
        if self.env is not None:
            config["env"] = self.env
        
        match self.transport:
            case ServerTransport.HTTP:
                config["url"] = self.url
            case ServerTransport.STDIO:
                config["command"] = self.command
                config["args"] = self.args

        return config

class DuplicateValueError(Exception):
    """Exception raised when a duplicate value is detected."""
    pass