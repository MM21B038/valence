from langchain_core.tools import tool
from agent.services.thread import Thread

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