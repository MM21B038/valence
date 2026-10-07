from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from dnd.models import Workspace
from protocol.serializers import WorkspaceContainerSerializer
from protocol.backend.manager_api import (
    ContainerManagerError,
    run_workspace,
    stop_workspace,
    stop_remove_workspace,
)


def _error_response(exc: ContainerManagerError) -> Response:
    return Response(
        status=exc.status_code,
        data={"detail": exc.message},
    )


class WorkspaceRunView(GenericAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceContainerSerializer

    def post(self, request, uuid):
        get_object_or_404(self.get_queryset(), uuid=uuid)
        try:
            result = run_workspace(str(uuid))
        except ContainerManagerError as exc:
            return _error_response(exc)

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(result).data,
        )


class WorkspaceStopView(GenericAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceContainerSerializer

    def post(self, request, uuid):
        get_object_or_404(self.get_queryset(), uuid=uuid)
        try:
            result = stop_workspace(str(uuid))
        except ContainerManagerError as exc:
            return _error_response(exc)

        return Response(
            status=status.HTTP_200_OK,
            data=self.get_serializer(result).data,
        )


class WorkspaceStopRemoveView(GenericAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceContainerSerializer

    def post(self, request, uuid):
        get_object_or_404(self.get_queryset(), uuid=uuid)
        try:
            result = stop_remove_workspace(str(uuid))
        except ContainerManagerError as exc:
            return _error_response(exc)

        return Response(
            status=status.HTTP_200_OK,
            data=self.get_serializer(result).data,
        )
