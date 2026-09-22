from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.shortcuts import get_object_or_404
from rest_framework import status
from agent.models import ThreadConfig, SystemPrompt, CompressionPrompt, ToolHideRuleModel
from agent.serializers import ThreadConfigSerializer

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

        if request.system_prompt:
            thread_config.system_prompt=system_prompt


        if request.compression_prompt:
            thread_config.compression_prompt=compression_prompt


        if request.compression_token_limit:
            thread_config.compression_token_limit=request.compression_token_limit


        if request.auto_hide_rule:
            thread_config.auto_hide_rule=request.auto_hide_rule

        if request.token_limit:
            thread_config.token_limit=request.token_limit

        if request.per_tool_token_limit:
            thread_config.per_tool_token_limit=request.per_tool_token_limit
        

        if request.tool_hide_rule:
            thread_config.tool_hide_rule.clear()
            for uuid in request.tool_hide_rules:
                tool_hide_rule = ToolHideRuleModel.objects.get(
                    uuid=uuid
                )

                thread_config.tool_hide_rules.add(tool_hide_rule)

        thread_config.save()

        return Response(
            ThreadConfigSerializer(thread_config).data
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

        serializer = self.get_serializer(
            self.get_queryset(),
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        system_prompt = SystemPrompt.objects.get(
            uuid=request.system_prompt
        )

        compression_prompt = CompressionPrompt.objects.get(
            uuid=request.compression_prompt
        )

        thread_config = ThreadConfig.objects.create(
            system_prompt=system_prompt,
            compression_prompt=compression_prompt,
            compression_token_limit=request.compression_token_limit,
            auto_hide_rule=request.auto_hide_rule,
            token_limit=request.token_limit,
            per_tool_token_limit=request.per_tool_token_limit
        )

        for uuid in request.tool_hide_rules:
            tool_hide_rule = ToolHideRuleModel.objects.get(
                uuid=uuid
            )

            thread_config.tool_hide_rules.add(tool_hide_rule)
        
        thread_config.save()

        return Response(
            ThreadConfigSerializer(thread_config).data
        )


