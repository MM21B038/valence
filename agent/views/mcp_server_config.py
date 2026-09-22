import asyncio
import threading
from asgiref.sync import sync_to_async
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.shortcuts import get_object_or_404
from agent.models import MCPServerConfig, ToolHideRuleModel, Prompt
from agent.serializers import MCPServerConfigSerializer, MCPServerConfigListSerializer
from agent.backend import get_server_tools, get_server_prompts

async def create_thread_hide_rule(server: MCPServerConfig):

    tools = await get_server_tools(server)

    for tool in tools:
        name=tool.name
        await sync_to_async(ToolHideRuleModel.objects.create)(
            server=server,
            name=name,
            message=f"[{name} result has been collapsed. Please refer to the latest tool result.]"
        )
    
async def add_prompts(server: MCPServerConfig):

    prompts = await get_server_prompts(server)

    for prompt in prompts:
        name = prompt.name
        await sync_to_async(Prompt.objects.create)(
            server=server,
            name=name,
            content=prompt.content
        )

class MCPServerConfigPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class MCPServerConfigView(GenericAPIView):

    queryset = MCPServerConfig.objects.all()
    serializer_class = MCPServerConfigSerializer

    def get(self, request, uuid):
        config = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )

        serializer = self.get_serializer(config)

        return Response(serializer.data)


    def put(self, request, uuid):
        config = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )

        serializer = self.get_serializer(
            config,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, uuid):
        config = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )

        serializer = self.get_serializer(
            config,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, uuid):
        config = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )

        config.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class MCPServerConfigListView(GenericAPIView):

    queryset = MCPServerConfig.objects.all()
    serializer_class = MCPServerConfigListSerializer
    pagination_class = MCPServerConfigPagination

    def get(self, request):

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True
            )

            return self.get_paginated_response(
                serializer.data
            )

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = MCPServerConfigSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        config = serializer.save()

        threading.Thread(
            target=lambda: asyncio.run(create_thread_hide_rule(config)),
            daemon=True,
        ).start()
        
        threading.Thread(
            target=lambda: asyncio.run(add_prompts(config)),
            daemon=True,
        ).start()

        return Response(
            MCPServerConfigSerializer(config).data,
            status=status.HTTP_201_CREATED
        )