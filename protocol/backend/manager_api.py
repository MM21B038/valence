from __future__ import annotations

import os
from collections import defaultdict
from typing import Any, Optional, Sequence
from uuid import UUID

import docker
from django.conf import settings
from docker.errors import APIError, ImageNotFound, NotFound

from dnd.enums import ComponentTypeChoices, WorkspaceTypeChoices
from dnd.models import Workspace
from protocol.models import AgentExecutorModel

WORKSPACE_LABEL = "valence.workspace_id"


class ContainerManagerError(Exception):
    """Raised when a Docker lifecycle operation fails."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def get_client() -> docker.DockerClient:
    return docker.from_env()


def _container_name(workspace_id: str, agent_executor_uuid: str) -> str:
    return f"{workspace_id}_{agent_executor_uuid}"


def _container_info(container) -> dict[str, Any]:
    container.reload()
    try:
        image = (
            container.image.tags[0]
            if container.image.tags
            else container.image.short_id
        )
    except (ImageNotFound, APIError):
        image = None
    return {
        "uuid": container.name,
        "container_name": container.name,
        "status": container.status,
        "image": image,
    }


def _remove_container_if_exists(client: docker.DockerClient, name: str) -> None:
    try:
        existing = client.containers.get(name)
    except NotFound:
        return
    try:
        existing.remove(force=True)
    except APIError as exc:
        raise ContainerManagerError(
            f"Failed to replace existing container {name}: {exc.explanation or exc}",
            status_code=500,
        ) from exc


def _ensure_network(client: docker.DockerClient, name: str):
    try:
        return client.networks.get(name)
    except NotFound:
        pass

    try:
        return client.networks.create(name, driver="bridge", check_duplicate=True)
    except APIError as exc:
        try:
            return client.networks.get(name)
        except NotFound:
            raise ContainerManagerError(
                f"Failed to create network {name}: {exc.explanation or exc}",
                status_code=500,
            ) from exc


def _remove_network(client: docker.DockerClient, name: str) -> None:
    try:
        network = client.networks.get(name)
    except NotFound:
        return

    try:
        network.remove()
    except APIError as exc:
        raise ContainerManagerError(
            f"Failed to remove network {name}: {exc.explanation or exc}",
            status_code=500,
        ) from exc


def _containers_for_workspace(
    client: docker.DockerClient,
    workspace_id: str,
) -> list:
    return client.containers.list(
        all=True,
        filters={"label": f"{WORKSPACE_LABEL}={workspace_id}"},
    )


def build_image() -> dict[str, Any]:
    client = get_client()
    image_tag = settings.AGENT_DOCKER_IMAGE
    try:
        image, _logs = client.images.build(
            path=settings.AGENT_DOCKER_BUILD_CONTEXT,
            tag=image_tag,
            rm=True,
        )
    except APIError as exc:
        raise ContainerManagerError(
            f"Failed to build image: {exc.explanation or exc}",
            status_code=500,
        ) from exc

    return {
        "image": image.tags[0] if image.tags else image_tag,
        "status": "built",
        "container_name": None,
        "uuid": None,
    }


def run_container(
    workspace_id: str,
    agent_executor_uuid: str,
    connected_to: Optional[Sequence[str]] = None,
    extra_networks: Optional[Sequence[str]] = None,
) -> dict[str, Any]:
    try:
        agent_executor = AgentExecutorModel.objects.get(uuid=agent_executor_uuid)
    except AgentExecutorModel.DoesNotExist as exc:
        raise ContainerManagerError(
            f"Agent executor {agent_executor_uuid} not found",
            status_code=404,
        ) from exc

    client = get_client()
    name = _container_name(workspace_id, agent_executor_uuid)
    image = settings.AGENT_DOCKER_IMAGE
    network = settings.AGENT_DOCKER_NETWORK
    port = int(agent_executor.port)

    command = ["python", "server.py", str(agent_executor.uuid)]
    for peer_uuid in connected_to or []:
        command.extend(["--connected-to", str(peer_uuid)])

    environment = {
        "DB_NAME": os.environ.get("DB_NAME", settings.DATABASES["default"]["NAME"]),
        "DB_USER": os.environ.get("DB_USER", settings.DATABASES["default"]["USER"]),
        "DB_PASSWORD": os.environ.get(
            "DB_PASSWORD", settings.DATABASES["default"]["PASSWORD"]
        ),
        "DB_HOST": "postgres",
        "DB_PORT": os.environ.get("DB_PORT", settings.DATABASES["default"]["PORT"]),
        "FIELD_ENCRYPTION_KEY": os.environ.get(
            "FIELD_ENCRYPTION_KEY", settings.FIELD_ENCRYPTION_KEY or ""
        ),
        "AGENT_BIND_HOST": "0.0.0.0",
        "AGENT_DOCKER_IMAGE": image,
        "AGENT_DOCKER_NETWORK": network,
        "AGENT_WORKSPACE_ID": str(workspace_id),
    }

    try:
        _remove_container_if_exists(client, name)
        container = client.containers.run(
            image=image,
            name=name,
            command=command,
            detach=True,
            network=network,
            ports={f"{port}/tcp": port},
            environment=environment,
            labels={WORKSPACE_LABEL: str(workspace_id)},
            restart_policy={"Name": "unless-stopped"},
        )
    except ImageNotFound as exc:
        _remove_container_if_exists(client, name)
        raise ContainerManagerError(
            f"Image {image} not found; build it first",
            status_code=404,
        ) from exc
    except APIError as exc:
        # Docker can leave a Created container behind when port bind fails.
        _remove_container_if_exists(client, name)
        explanation = exc.explanation or str(exc)
        if "port is already allocated" in explanation.lower() or "Bind for" in explanation:
            raise ContainerManagerError(
                f"Port {port} is already in use (another workspace may be running "
                f"the same agent executor). Stop the other workspace first.",
                status_code=409,
            ) from exc
        status_code = 409 if "Conflict" in str(exc) else 500
        raise ContainerManagerError(
            f"Failed to run container: {explanation}",
            status_code=status_code,
        ) from exc

    for extra in extra_networks or []:
        try:
            client.networks.get(extra).connect(container)
        except APIError as exc:
            raise ContainerManagerError(
                f"Failed to connect container to network {extra}: {exc.explanation or exc}",
                status_code=500,
            ) from exc

    return _container_info(container)


def _agent_executor_graph(workspace: Workspace) -> tuple[set[str], dict[str, list[str]]]:
    """Return executor UUIDs involved and source -> target peer map from connections."""
    peer_map: dict[str, list[str]] = defaultdict(list)
    involved: set[str] = set()

    for connection in workspace.connections.all():
        source = connection.source
        target = connection.target
        if (
            source.type != ComponentTypeChoices.AGENT_EXECUTOR
            or target.type != ComponentTypeChoices.AGENT_EXECUTOR
        ):
            continue
        if not source.component_uuid or not target.component_uuid:
            continue

        source_id = str(source.component_uuid)
        target_id = str(target.component_uuid)
        involved.add(source_id)
        involved.add(target_id)
        peer_map[source_id].append(target_id)

    return involved, peer_map


def _agent_executor_components(workspace: Workspace) -> list[str]:
    return [
        str(component.component_uuid)
        for component in workspace.components.all()
        if (
            component.type == ComponentTypeChoices.AGENT_EXECUTOR
            and component.component_uuid is not None
        )
    ]


def run_workspace(workspace_id: str | UUID) -> dict[str, Any]:
    workspace_id = str(workspace_id)
    try:
        workspace = Workspace.objects.prefetch_related(
            "components",
            "connections__source",
            "connections__target",
        ).get(uuid=workspace_id)
    except Workspace.DoesNotExist as exc:
        raise ContainerManagerError(
            f"Workspace {workspace_id} not found",
            status_code=404,
        ) from exc

    client = get_client()
    network_name: str | None = None
    extra_networks: list[str] = []

    if workspace.type == WorkspaceTypeChoices.A2A:
        network_name = workspace_id
        _ensure_network(client, network_name)
        extra_networks = [network_name]
        involved, peer_map = _agent_executor_graph(workspace)
        executor_ids = sorted(involved)
        if not executor_ids:
            # Fall back to all agent-executor components on the canvas.
            executor_ids = _agent_executor_components(workspace)
            peer_map = {}
    else:
        executor_ids = _agent_executor_components(workspace)
        peer_map = {}

    if not executor_ids:
        raise ContainerManagerError(
            f"Workspace {workspace_id} has no agent-executor components to run",
            status_code=400,
        )

    containers: list[dict[str, Any]] = []
    for executor_id in executor_ids:
        containers.append(
            run_container(
                workspace_id=workspace_id,
                agent_executor_uuid=executor_id,
                connected_to=peer_map.get(executor_id, []),
                extra_networks=extra_networks,
            )
        )

    return {
        "network": network_name,
        "containers": containers,
    }


def stop_workspace(workspace_id: str | UUID) -> dict[str, Any]:
    workspace_id = str(workspace_id)
    client = get_client()
    containers = _containers_for_workspace(client, workspace_id)

    if not containers:
        return {
            "network": None,
            "containers": [
                {
                    "uuid": None,
                    "container_name": None,
                    "status": "not_found",
                    "image": None,
                }
            ],
        }

    results: list[dict[str, Any]] = []
    for container in containers:
        try:
            container.stop()
        except APIError as exc:
            raise ContainerManagerError(
                f"Failed to stop container {container.name}: {exc.explanation or exc}",
                status_code=500,
            ) from exc
        results.append(_container_info(container))

    return {
        "network": None,
        "containers": results,
    }


def stop_remove_workspace(workspace_id: str | UUID) -> dict[str, Any]:
    workspace_id = str(workspace_id)
    client = get_client()
    containers = _containers_for_workspace(client, workspace_id)

    results: list[dict[str, Any]] = []
    if not containers:
        results.append(
            {
                "uuid": None,
                "container_name": None,
                "status": "not_found",
                "image": None,
            }
        )
    else:
        for container in containers:
            name = container.name
            try:
                image = (
                    container.image.tags[0]
                    if container.image.tags
                    else container.image.short_id
                )
            except (ImageNotFound, APIError):
                image = None
            try:
                container.remove(force=True)
            except APIError as exc:
                raise ContainerManagerError(
                    f"Failed to stop-remove container {name}: {exc.explanation or exc}",
                    status_code=500,
                ) from exc
            results.append(
                {
                    "uuid": name,
                    "container_name": name,
                    "status": "removed",
                    "image": image,
                }
            )

    network_name = workspace_id
    _remove_network(client, network_name)

    return {
        "network": network_name,
        "containers": results,
    }
