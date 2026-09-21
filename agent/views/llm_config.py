from rest_framework.generics import GenericAPIView
from agent.models import LLMConfig
from agent.serializers import LLMConfigSerializer

class LLMConfigView(GenericAPIView):

    serializer_class = LLMConfigSerializer

    def get(self, request):
        configs = LLMConfig.objects.all()
        serializer = self.get_serializer(configs, many=True)
        return Response(serializer.data)

