import os
from typing import List, Dict
import openai


class OpenAIAgent:
    """Wrapper around OpenAI chat completion API."""

    def __init__(self, system_prompt: str, model: str = "gpt-4-turbo") -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY not set")
        self.client = openai.OpenAI(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = model

    def run(self, input_text: str) -> str:
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content
