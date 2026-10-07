from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

from protocol.serializers import AgentExecutorContainerSerializer
from protocol.backend.manager_api import (
    ContainerManagerError,
    build_image,
)


def _error_response(exc: ContainerManagerError) -> Response:
    return Response(
        status=exc.status_code,
        data={"detail": exc.message},
    )


class AgentExecutorImageBuildView(GenericAPIView):
    serializer_class = AgentExecutorContainerSerializer

    def post(self, request):
        try:
            result = build_image()
        except ContainerManagerError as exc:
            return _error_response(exc)

        serializer = self.get_serializer(result)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
