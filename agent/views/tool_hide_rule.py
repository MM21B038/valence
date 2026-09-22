from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from agent.models import ToolHideRuleModel
from agent.serializers import ToolHideRuleSerializer, ToolHideRuleListSerializer

class ToolHideRuleView(GenericAPIView):

    queryset = ToolHideRuleModel.objects.all()
    serailizer_class = ToolHideRuleSerializer

    def get(self, request, uuid):

        rule = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )

        serializer = self.get_serializer(rule)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def patch(self, request, uuid):
        rule = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )

        serializer = self.get_serializer(
            rule,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

class ToolHideRuleListView(GenericAPIView):

    queryset = ToolHideRuleModel.objects.all()
    serializer_class = ToolHideRuleListSerializer

    def get(self, request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

