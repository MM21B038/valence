from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dnd.models import Connection
from dnd.serializers import ConnectionSerializer, ComponentSerializer

class ConnectionView(GenericAPIView):

    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

    def get(self, request, uuid):
        connection = get_object_or_404(self.get_queryset(), uuid=uuid)
        source = ComponentSerializer.objects.get(uuid=connection.source.uuid)
        target = ComponentSerializer.objects.get(uuid=connection.target.uuid)

        return Response(
            status = status.HTTP_200_OK,
            data = {
                'uuid' : connection.uuid,
                'source': source.data,
                'target': target.data,
            },
        )

    def patch(self, request, uuid):
        connection = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(
            connection,
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
        connection = get_object_or_404(self.get_queryset(), uuid=uuid)
        connection.delete()

        return Response(
            status = status.HTTP_204_NO_CONTENT,
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status = status.HTTP_201_CREATED,
            data = serializer.data,
        )
        
        