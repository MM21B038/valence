from typing import Optional
from pydantic import BaseModel

class ToolHideRule(BaseModel):
    name: str
    message: str

class AutoToolHideRule(BaseModel):
    token_limit: int
    per_tool_token_limit: Optional[int] = None
