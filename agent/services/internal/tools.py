from langchain_core.tools import tool
from agent.services.thread import Thread
from agent.models import InternalTool

class InternalTools:
    @classmethod
    def tools(cls):
        @tool("collapsed_tool_result", description="Fetch old collapsed tool result using tool call id.")
        def collapsed_tool_result(tool_call_id: str) -> str:
            file_path = Thread.get_tool_result_path() / tool_call_id
            
            try:
                return file_path.read_text(encoding="utf-8")
            except Exception as e:
                return str(e)

        return [collapsed_tool_result]

def manage_internal_tools():
    tools = [tool.name for tool in InternalTool.objects.all()]

    for tool in InternalTools.tools():
        if tool.name not in tools:
            InternalTool.objects.create(name=tool.name, description=tool.description)
            tools.append(tool.name)

    tools = [tool.name for tool in InternalTools.tools()]
    
    for tool in InternalTool.objects.all():
        if tool.name not in tools:
            tool.delete()