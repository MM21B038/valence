from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from dnd.models import Workspace
from dnd.serializers import (
    WorkspaceSerializer,
    WorkspaceListSerializer,
    WorkspaceDetailSerializer,
)


class WorkspaceView(GenericAPIView):

    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkspaceDetailSerializer
        return WorkspaceSerializer

    def get(self, request, uuid):
        workspace = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(workspace)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def patch(self, request, uuid):
        workspace = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(
            workspace,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def delete(self, request, uuid):
        workspace = get_object_or_404(self.get_queryset(), uuid=uuid)
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkspaceListCreateView(GenericAPIView):

    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

    def get(self, request):
        workspace = self.filter_queryset(self.get_queryset())
        serializer = WorkspaceListSerializer(workspace, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
