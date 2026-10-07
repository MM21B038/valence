from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from protocol.models import AgentExecutorModel
from protocol.serializers import AgentExecutorSerializer, AgentExecutorListSerializer

class AgentExecutorView(GenericAPIView):

    queryset = AgentExecutorModel.objects.all()
    serializer_class = AgentExecutorSerializer

    def get(self, request, uuid):
        agent_executor = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(agent_executor)

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def patch(self, request, uuid):
        agent_executor = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(
            agent_executor,
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
        agent_executor = get_object_or_404(self.get_queryset(), uuid=uuid)
        agent_executor.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

class AgentExecutorListCreateView(GenericAPIView):

    queryset = AgentExecutorModel.objects.all()
    serializer_class = AgentExecutorSerializer
   
    def get(self, request):
        agent_executor = self.get_queryset()
        serializer = AgentExecutorListSerializer(agent_executor, many=True)
        # serializer = self.get_serializer(agent_executor, many=True)

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