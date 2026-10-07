import os
import re
import uvicorn
import typer
import asyncio
from asgiref.sync import sync_to_async
from typing import List, Optional
from fastapi import FastAPI
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes, create_rest_routes
from a2a.types import AgentCard, AgentInterface
from protocol.models import AgentExecutorModel
from protocol.backend import get_agent_card, get_request_handler
from protocol.errors import GetAgentCardError
from protocol.enums import TransportProtocolChoices

t = typer.Typer()

_URL_HOST_RE = re.compile(r"^(?P<scheme>https?://)(?P<host>[^/:]+)(?P<rest>.*)$")


def _rewrite_interface_host(interface: AgentInterface, host: str) -> AgentInterface:
    match = _URL_HOST_RE.match(interface.url)
    if not match:
        return interface
    return AgentInterface(
        url=f"{match.group('scheme')}{host}{match.group('rest')}",
        protocol_binding=interface.protocol_binding,
    )


def _rewrite_peer_card(card: AgentCard, container_host: str) -> AgentCard:
    rewritten = [
        _rewrite_interface_host(interface, container_host)
        for interface in card.supported_interfaces
    ]
    updated = AgentCard()
    updated.CopyFrom(card)
    del updated.supported_interfaces[:]
    updated.supported_interfaces.extend(rewritten)
    return updated


async def _fetch_cards(connected_to: List[str], workspace_id: Optional[str]) -> List:
    if not connected_to:
        return []

    def _load_peers():
        agents = list(
            AgentExecutorModel.objects.filter(uuid__in=connected_to).select_related(
                "agent_card"
            )
        )
        # Resolve FKs here — accessing agent.agent_card in the async event
        # loop raises SynchronousOnlyOperation.
        return [(agent, agent.agent_card) for agent in agents]

    peers = await sync_to_async(_load_peers)()

    cards = await asyncio.gather(
        *(get_agent_card(card) for _, card in peers)
    )

    result = []
    for (agent, _), card in zip(peers, cards):
        if isinstance(card, GetAgentCardError):
            continue
        if workspace_id:
            container_host = f"{workspace_id}_{agent.uuid}"
            card = _rewrite_peer_card(card, container_host)
        result.append(card)

    return result


async def build_and_run_agent(agent_executor_uuid: str, connected_to: List[str]):
    agent_executor = await sync_to_async(
        AgentExecutorModel.objects.get
    )(uuid=agent_executor_uuid)

    agent_card = await get_agent_card(await sync_to_async(lambda: agent_executor.agent_card)())

    if isinstance(agent_card, GetAgentCardError):
        return agent_card

    workspace_id = os.getenv("AGENT_WORKSPACE_ID") or None
    cards = await _fetch_cards(connected_to, workspace_id)
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

    bind_host = os.getenv("AGENT_BIND_HOST") or agent_executor.host
    config = uvicorn.Config(
        app,
        host=bind_host,
        port=agent_executor.port,
    )
    server = uvicorn.Server(config)
    await server.serve()

@t.command()
def main(agent_executor_uuid: str, connected_to: Optional[List[str]] = typer.Option(None, "--connected-to")):
    asyncio.run(build_and_run_agent(agent_executor_uuid, connected_to or []))
