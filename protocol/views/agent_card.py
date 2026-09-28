from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from protocol.models import AgentCardModel
from protocol.serializers import AgentCardSerializer, AgentCardListSerializer

class AgentCardView(GenericAPIView):

    queryset = AgentCardModel.objects.all()
    serializer_class = AgentCardSerializer

    def get(self, request, uuid):
        agent_card = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(agent_card)

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def patch(self, request, uuid):
        agent_card = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(
            agent_card,
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
        agent_card = get_object_or_404(self.get_queryset(), uuid=uuid)
        agent_card.delete()

        return Reponse(
            status = status.HTTP_204_NO_CONTENT,
        )

class AgentCardListView(GenericAPIView):

    queryset = AgentCardModel.objects.all()
    serializer_class = AgentCardListSerializer

    def get(self, request):
        agent_card = self.get_queryset()
        serializer = self.get_serializer(agent_card, many=True)

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def post(self, request):
        serializer = AgentCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status = status.HTTP_201_CREATED,
            data = serializer.data,
        )