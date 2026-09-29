from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dnd.models import AgentSkillStack
from dnd.serializers import AgentSkillStackSerializer

class AgentSkillStackView(GenericAPIView):

    queryset = AgentSkillStack.objects.all()
    serializer_class = AgentSkillStackSerializer

    def get(self, request, uuid):
        agent_skill_stack = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(agent_skill_stack)

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
        agent_skill_stack = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(
            agent_skill_stack,
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
        agent_skill_stack = get_object_or_404(self.get_queryset(), uuid=uuid)
        agent_skill_stack.delete()
        
        return Response(
            status = status.HTTP_204_NO_CONTENT,
        )