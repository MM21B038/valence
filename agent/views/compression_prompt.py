from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from agent.models import CompressionPrompt
from agent.serializers import CompressionPromptSerializer

class CompressionPromptView(GenericAPIView):

    queryset = CompressionPrompt.objects.all()
    serializer_class = CompressionPromptSerializer

    def get(self, request, uuid):
        prompt = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )
        serializer = self.get_serializer(prompt)
        return Response(serializer.data)

    def put(self, request, uuid):
        prompt = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )
        serializer = self.get_serializer(
            prompt,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def put(self, request, uuid):
        prompt = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )
        serializer = self.get_serializer(
            prompt,
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
        prompt = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )
        prompt.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class CompressionPromptListView(GenericAPIView):

    queryset = CompressionPrompt.objects.all()
    serializer_class = CompressionPromptSerializer

    def get(self, request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data
        )