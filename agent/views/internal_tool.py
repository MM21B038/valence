from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from agent.models import InternalTool
from agent.serializers import InternalToolSerializer

class InternalToolListView(GenericAPIView):

    queryset = InternalTool.objects.all()
    serializer_class = InternalToolSerializer

    def get(self, request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )

        return Response(serializer.data)