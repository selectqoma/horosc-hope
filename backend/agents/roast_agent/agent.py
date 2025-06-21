from ..scraper_agent.scraper import normalize
from ...core.agents_sdk_wrapper import OpenAIAgent
from .prompt_templates import ROAST_PROMPT


def run(text: str) -> str:
    cleaned = normalize(text)
    prompt = ROAST_PROMPT.format(text=cleaned)
    agent = OpenAIAgent(system_prompt="You are Scorpiobot, the roast master.")
    return agent.run(prompt)
