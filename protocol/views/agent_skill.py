from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from protocol.models import AgentSkillModel
from protocol.serializers import AgentSkillSerializer, AgentSkillListSerializer

class AgentSkillView(GenericAPIView):

    queryset = AgentSkillModel.objects.all()
    serializer_class = AgentSkillSerializer

    def get(self, request, uuid):

        agent_skill = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(agent_skill)

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def patch(self, request, uuid):

        agent_skill = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(
            agent_skill,
            data = request.data,
            partial = True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def delete(self, request, uuid):

        agent_skill = get_object_or_404(self.get_queryset(), uuid=uuid)
        agent_skill.delete()

        return Response(
            status = status.HTTP_204_NO_CONTENT,
        )


class AgentSkillListView(GenericAPIView):

    queryset = AgentSkillModel.objects.all()
    serializer_class = AgentSkillListSerializer

    def get(self, request):
        agent_skills = self.get_queryset()
        serializer = self.get_serializer(agent_skills, many=True)

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def post(self, request):
        serializer = AgentSkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status = status.HTTP_201_CREATED,
            data = serializer.data,
        )

