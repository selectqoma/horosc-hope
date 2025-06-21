from fastapi import APIRouter, HTTPException
from ...agents.scraper_agent.agent import run_scraper
from ...agents.roast_agent import agent as roast_agent
from ..utils.caching import load_from_cache, save_to_cache

router = APIRouter()


@router.get("/horoscope/{sign}/daily")
def get_daily_horoscope(sign: str):
    cached = load_from_cache(sign, "daily")
    if cached is None:
        text = run_scraper(sign, "daily")
        save_to_cache(sign, "daily", text)
    else:
        text = cached
    roasted = roast_agent.run(text)
    return {"sign": sign, "roast": roasted}


@router.get("/sign/{sign}/description")
def get_sign_description(sign: str):
    cached = load_from_cache(sign, "description")
    if cached is None:
        # Placeholder for future implementation
        description = run_scraper(sign, "daily")
        save_to_cache(sign, "description", description)
    else:
        description = cached
    roasted = roast_agent.run(description)
    return {"sign": sign, "personality": roasted}
