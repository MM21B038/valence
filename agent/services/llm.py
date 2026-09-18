from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter
from pydantic import SecretStr
from agent.enums import LLMProvider


class LLM:
    def __init__(
        self, 
        provider: LLMProvider, 
        model: str, 
        base_url: Optional[str] = None, 
        api_key: Optional[str] = None
    ):
        self.provider = provider
        self.model = model
        self.base_url = base_url
        self.api_key = api_key

    def connect(self):
        api_key = SecretStr(self.api_key) if self.api_key is not None else None

        if self.provider == LLMProvider.OPENAI:
            return ChatOpenAI(
                model=self.model,
                api_key=api_key
            )
            
        elif self.provider == LLMProvider.OPENAI_COMPATIBLE:
            return ChatOpenAI(
                model=self.model,
                base_url=self.base_url,
                api_key=api_key,
            )

        elif self.provider == LLMProvider.OPENROUTER:
            return ChatOpenRouter(
                model=self.model,
                api_key=api_key,
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")