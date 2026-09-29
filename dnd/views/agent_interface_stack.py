from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dnd.models import AgentInterfaceStack
from dnd.serializers import AgentInterfaceStackSerializer

class AgentInterfaceStackView(GenericAPIView):

    queryset = AgentInterfaceStack.objects.all()
    serializer_class = AgentInterfaceStackSerializer

    def get(self, request, uuid):
        agent_interface_stack = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(agent_interface_stack)

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status = status.HTTP_201_CREATED,
            data = serializer.data,
        )
    
    def patch(self, request, uuid):
        agent_interface_stack = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(
            agent_interface_stack,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )
    
    def delete(self, request, uuid):
        agent_interface_stack = get_object_or_404(self.get_queryset(), uuid=uuid)
        agent_interface_stack.delete()
        
        return Response(
            status = status.HTTP_204_NO_CONTENT,
        )