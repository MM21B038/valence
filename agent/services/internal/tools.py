import asyncio
import httpx
import json
from a2a.client import ClientConfig, create_client
from a2a.client.card_resolver import A2ACardResolver
from a2a.helpers import get_artifact_text, get_message_text, new_text_message
from a2a.types import (
    Role,
    SendMessageRequest,
    SubscribeToTaskRequest,
    GetTaskRequest,
    ListTasksRequest,
    TaskState,
)
from a2a.utils import TransportProtocol
from pydantic import BaseModel, Field, ConfigDict
from langchain_core.tools import tool
from agent.services.thread import Thread
from agent.models import InternalTool

class A2ARequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    url: str = Field(..., description="Request url")
    protocol: TransportProtocol = Field(default=TransportProtocol.JSONRPC, description="Transport Protocol")
    text: str = Field(..., description="Query/Message/Text to send to the agent")
    boolean: bool = False

class A2ATaskRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    url: str = Field(..., description="Request url")
    protocol: TransportProtocol = Field(default=TransportProtocol.JSONRPC, description="Transport Protocol")
    task_id: str = Field(..., description="Respective agent task id")

class InternalTools:
    @classmethod
    def tools(cls):
        @tool("collapsed_tool_result", description="Fetch old collapsed tool result using tool call id.")
        async def collapsed_tool_result(tool_call_id: str) -> str:
            file_path = Thread.get_tool_result_path() / tool_call_id
            
            try:
                return file_path.read_text(encoding="utf-8")
            except Exception as e:
                return str(e)

        @tool("a2a_invoke")
        async def a2a_invoke(
            request: A2ARequest 
        ):
            """
            Use it to assign task/work to an another agent using the A2A Protocol
            """
            async with httpx.AsyncClient(timeout=None) as http:
                agent_card = await A2ACardResolver(http, request.url).get_agent_card()
                
                allowed_protocols = [p.protocol_binding for p in agent_card.supported_interfaces]
                client = await create_client(
                    agent_card,
                    client_config = ClientConfig(
                        supported_protocol_bindings = [
                            request.protocol 
                            if request.protocol in allowed_protocols
                            else allowed_protocols[0]
                        ],
                        httpx_client = http,
                    ),
                )
            
                try:
                    message_request = SendMessageRequest(
                        message=new_text_message(
                            text=request.text, 
                            role=Role.ROLE_USER,
                        ),
                    )
                    response = None
                    async for reply in client.send_message(message_request):
                        response = reply
                        break
                finally:
                    await client.close()

            if response is None:
                return str(RuntimeError("A2A client returned no response"))

            return json.dumps(
                {
                    "task_id": response.task.id,
                    "task_context_id": response.task.context_id,
                    "terminate_state": TaskState.Name(response.task.status.state),
                    "text": response.task.status.message.parts[0].text,
                }
            )

        @tool("a2a_get_task")
        async def a2a_get_task(
            request: A2ATaskRequest
        ):
            """
            Use it to assign task/work to an another agent using the A2A Protocol
            """
            async with httpx.AsyncClient(timeout=None) as http:
                agent_card = await A2ACardResolver(http, request.url).get_agent_card()
                
                allowed_protocols = [p.protocol_binding for p in agent_card.supported_interfaces]
                client = await create_client(
                    agent_card,
                    client_config = ClientConfig(
                        supported_protocol_bindings = [
                            request.protocol 
                            if request.protocol in allowed_protocols
                            else allowed_protocols[0]
                        ],
                        httpx_client = http,
                    ),
                )
            
                try:
                    task_request = GetTaskRequest(
                        id=request.task_id
                    )
            
                    task = await client.get_task(task_request)
                finally:
                    await client.close()

            return json.dumps(
                {
                    "task_id": task.id,
                    "task_context_id": task.context_id,
                    "terminate_state": TaskState.Name(task.status.state),
                    "text": task.status.message.parts[0].text,
                }
            )  

        return [collapsed_tool_result, a2a_invoke, a2a_get_task]

def manage_internal_tools():
    tools = [tool.name for tool in InternalTool.objects.all()]

    for tool in InternalTools.tools():
        if tool.name not in tools:
            InternalTool.objects.create(name=tool.name, description=tool.description)
            tools.append(tool.name)

    tools = [tool.name for tool in InternalTools.tools()]
    
    for tool in InternalTool.objects.all():
        if tool.name not in tools:
            tool.delete()