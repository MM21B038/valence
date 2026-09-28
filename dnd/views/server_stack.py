from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dnd.models import ServerStack
from dnd.serializers import ServerStackSerializer

class ServerStackView(GenericAPIView):

    queryset = ServerStack.objects.all()
    serializer_class = ServerStackSerializer

    def get(self, request, uuid):
        server_stack = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(server_stack)

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
        server_stack = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(
            server_stack,
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
        server_stack = get_object_or_404(self.get_queryset(), uuid=uuid)
        server_stack.delete()
        
        return Response(
            status = status.HTTP_204_NO_CONTENT,
        )