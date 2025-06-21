import json
from pydantic import BaseModel, Field
from backend.agents.scraper_agent.scraper import normalize
from backend.core.agents_sdk_wrapper import OpenAIAgent
from .prompt_templates import ROAST_PROMPT, CATEGORIZED_ROAST_PROMPT, BIRTH_CHART_SYNTHESIS_PROMPT


class CategorizedRoast(BaseModel):
    """Pydantic model for categorized horoscope roasts."""
    overall: str = Field(description="Comprehensive overall roast summary (3-4 sentences)")
    love: str = Field(description="Roast about love life (1-2 sentences)")
    work: str = Field(description="Roast about work/career (1-2 sentences)")
    social: str = Field(description="Roast about social life (1-2 sentences)")


def run(text: str, language: str = "English") -> str:
    cleaned = normalize(text)
    prompt = ROAST_PROMPT.format(text=cleaned, language=language)
    agent = OpenAIAgent(system_prompt="You are Scorpiobot, the roast master.")
    return agent.run(prompt)


def run_categorized(text: str, language: str = "English") -> dict:
    """Generate categorized roasts for Love, Work, Social Life, and Overall."""
    cleaned = normalize(text)
    prompt = CATEGORIZED_ROAST_PROMPT.format(text=cleaned, language=language)
    
    # Use Pydantic model for structured output
    agent = OpenAIAgent(
        system_prompt="You are Scorpiobot, the roast master. Always respond with valid JSON that matches the required schema.",
        response_format=CategorizedRoast
    )
    
    try:
        response = agent.run(prompt)
        # If the agent returns a Pydantic model, convert to dict
        if isinstance(response, CategorizedRoast):
            return response.model_dump()
        # If it's a string, try to parse as JSON
        elif isinstance(response, str):
            roast_data = json.loads(response)
            # Validate with Pydantic
            validated = CategorizedRoast(**roast_data)
            return validated.model_dump()
        else:
            # Fallback
            return response
    except (json.JSONDecodeError, ValueError, Exception) as e:
        # Fallback if anything fails
        return {
            "overall": "Overall, even the AI is confused by your cosmic energy. Your chart is so chaotic that even machine learning algorithms give up trying to decode it.",
            "love": "Your love life is as unpredictable as this error message.",
            "work": "Your career path is as unclear as this malformed response.",
            "social": "Your social skills need debugging, just like this code."
        }


def run_birth_chart_synthesis(planet_roasts: dict, language: str = "English") -> str:
    """Generate a synthesis roast that combines all planet roasts into one comprehensive analysis."""
    # Format planet roasts into a readable string
    roasts_text = "\n".join([f"{planet}: {roast}" for planet, roast in planet_roasts.items()])
    
    prompt = BIRTH_CHART_SYNTHESIS_PROMPT.format(planet_roasts=roasts_text, language=language)
    agent = OpenAIAgent(system_prompt="You are Scorpiobot, the roast master.")
    
    try:
        return agent.run(prompt)
    except Exception as e:
        # Fallback if anything fails
        return "Your cosmic blueprint is so complex that even the universe's best roast algorithm crashed trying to decode it. Consider this a blessing in disguise, because the truth might have been too brutal to handle."
