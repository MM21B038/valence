import asyncio
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.shortcuts import get_object_or_404
from agent.enums import LLMProvider
from agent.models import LLMConfig
from agent.serializers import LLMConfigSerializer
from agent.services import LLM, Thread, Agent
from agent.backend import get_mcp_tools_by_id
from langchain_core.messages import SystemMessage, HumanMessage

class LLMConfigPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class LLMProviderOptionView(GenericAPIView):

    def get(self, request):
        return Response(
            status=status.HTTP_200_OK,
            data={
                "providers": [
                    value
                    for value, _ in LLMProvider.choices
                ]
            }
        )

class LLMConfigView(GenericAPIView):

    queryset = LLMConfig.objects.all()
    serializer_class = LLMConfigSerializer

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

class LLMConfigListView(GenericAPIView):

    queryset = LLMConfig.objects.all()
    serializer_class = LLMConfigSerializer
    pagination_class = LLMConfigPagination

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
        serializer = LLMConfigSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        config = serializer.save()

        return Response(
            LLMConfigSerializer(config).data,
            status=status.HTTP_201_CREATED
        )

class LLMChatView(GenericAPIView):

    queryset = LLMConfig.objects.all()

    def post(self, request, uuid):
        message = request.data.get("message")
        servers = request.data.get("servers") or []

        tools = asyncio.run(get_mcp_tools_by_id(servers))

        config = get_object_or_404(
            self.get_queryset(),
            uuid=uuid
        )

        try:

            llm = LLM.from_config(config)

            agent = Agent(
                model=llm,
                tools=tools
            )

            thread = Thread()

            thread.append(SystemMessage("You are the conversational agent and extroert. your name is `valence`"))
            thread.append(HumanMessage(message))

            content = agent.invoke(thread).content

        except Exception as e:
            content = str(e)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": content
            }
        )
