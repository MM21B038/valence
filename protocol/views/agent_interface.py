from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from protocol.models import AgentInterfaceModel
from protocol.serializers import AgentInterfaceSerializer

class AgentInterfaceView(GenericAPIView):

    queryset = AgentInterfaceModel.objects.all()
    serializer_class = AgentInterfaceSerializer

    def get(self, request):
        agent_interface = self.get_queryset()
        serializer = self.get_serializer(agent_interface, many=True)

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def post(self, request):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status = status.HTTP_201_CREATED,
            data = serializer.data,
        )

    def patch(self, request, uuid):
        agent_interface = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = get_serializer(
            agent_interface,
            data = request.data,
            partial = True,
        )
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def delete(self, request, uuid):
        agent_interface = get_object_or_404(self.get_queryset(), uuid=uuid)
        agent_interface.delete()

        return Response(
            status = status.HTTP_401_NO_CONTENT,
        )