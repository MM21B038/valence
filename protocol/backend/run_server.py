import uvicorn
import typer
import asyncio
from asgiref.sync import sync_to_async
from typing import List, Optional
from fastapi import FastAPI
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes, create_rest_routes
from protocol.models import AgentExecutorModel
from protocol.backend import get_agent_card, get_request_handler
from protocol.errors import GetAgentCardError
from protocol.enums import TransportProtocolChoices

t = typer.Typer()

async def _fetch_cards(connected_to: List[str]):
    cards = []
    for uuid in connected_to:
        agent = await sync_to_async(
            AgentExecutorModel.objects.get
        )(uuid=uuid)

        if isinstance(agent, AgentExecutorModel):
            cards.append(await get_agent_card(agent.agent_card))
    return cards

async def build_and_run_agent(agent_executor_uuid: str, connected_to: List[str]):
    agent_executor = await sync_to_async(
        AgentExecutorModel.objects.get
    )(uuid=agent_executor_uuid)

    agent_card = await get_agent_card(agent_executor.agent_card)

    if isinstance(agent_card, GetAgentCardError):
        return agent_card
    
    cards = await _fetch_cards(connected_to)
    request_handler = await get_request_handler(agent_executor, agent_card, cards)

    app = FastAPI()
    for route in create_agent_card_routes(agent_card=agent_card):
        app.router.routes.append(route)

    for interface in agent_card.supported_interfaces:

        if interface.protocol_binding == TransportProtocolChoices.HTTP_JSON:
            for route in create_rest_routes(request_handler = request_handler):
                app.router.routes.append(route)
                
        if interface.protocol_binding == TransportProtocolChoices.JSONRPC:
            rpc_url = agent_executor.rpc_url or "/"
            for route in create_jsonrpc_routes(request_handler = request_handler, rpc_url = rpc_url):
                app.router.routes.append(route)

    uvicorn.run(app, host=agent_executor.host, port=agent_executor.port)

@t.command()
def main(agent_executor_uuid: str, connected_to: Optional[List[str]] = None):
    asyncio.run(build_and_run_agent(agent_executor_uuid, connected_to or []))