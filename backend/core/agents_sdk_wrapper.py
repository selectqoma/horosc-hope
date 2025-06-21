from typing import List, Dict, Optional, Type, Union
import openai
from pydantic import BaseModel
from .config import Config


class OpenAIAgent:
    """Wrapper around OpenAI chat completion API."""

    def __init__(self, system_prompt: str, model: str = "gpt-4o-mini", response_format: Optional[Type[BaseModel]] = None) -> None:
        api_key = Config.get_openai_api_key()
        self.client = openai.OpenAI(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = model
        self.response_format = response_format

    def run(self, input_text: str) -> Union[str, BaseModel]:
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": input_text},
        ]
        
        # Use structured outputs if response_format is provided
        if self.response_format:
            try:
                response = self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=messages,
                    response_format=self.response_format,
                )
                return response.choices[0].message.parsed
            except Exception:
                # Fallback to regular completion if structured output fails
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                )
                return response.choices[0].message.content
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return response.choices[0].message.content
