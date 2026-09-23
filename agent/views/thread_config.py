from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from agent.models import ThreadConfig, SystemPrompt, CompressionPrompt, ToolHideRuleModel
from agent.serializers import ThreadConfigSerializer, ThreadConfigListSerializer

class ThreadConfigView(GenericAPIView):

    queryset = ThreadConfig.objects.all()
    serializer_class = ThreadConfigSerializer

    def get(self, request, uuid):
        thread_config = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )

        serializer = self.get_serializer(thread_config)

        return Response(serializer.data)

    def patch(self, request, uuid):

        thread_config = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )

        serializer = self.get_serializer(
            thread_config,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )


    def delete(self, request, uuid):
        thread_config = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )
        thread_config.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ThreadConfigListView(GenericAPIView):

    queryset = ThreadConfig.objects.all()
    serializer_class = ThreadConfigSerializer

    def get(self, request):

        serializer = ThreadConfigListSerializer(
            self.get_queryset(),
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        thread_config = serializer.save()

        return Response(
            self.get_serializer(thread_config).data,
            status=status.HTTP_201_CREATED
        )


