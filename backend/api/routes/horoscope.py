import logging
import requests
from fastapi import APIRouter, HTTPException, Query
from ...agents.scraper_agent.agent import run_scraper
from ...agents.roast_agent import agent as roast_agent
from ..utils.caching import load_from_cache, save_to_cache
from ...core.zodiac_calculator import get_zodiac_sign, get_sign_info
from ...core.birth_chart_calculator import calculate_birth_chart, generate_birth_chart_summary
from ...core.geocoder import search_cities_with_suggestions, get_city_coordinates_with_rate_limit

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint to monitor application status."""
    try:
        # Test external API (optional fallback)
        response = requests.get(
            "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign=Aries&day=TODAY", 
            timeout=3
        )
        external_api_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception as e:
        logger.warning(f"External API health check failed: {e}")
        external_api_status = "unavailable"
    
    return {
        "status": "healthy",
        "external_api": external_api_status,
        "local_generation": "enabled",
        "message": "HoroscHope API is running with local horoscope generation"
    }


@router.get("/search-cities")
def search_cities(query: str = Query(..., description="City name to search for"), limit: int = Query(5, description="Maximum number of results")):
    """Search for cities and return suggestions."""
    try:
        if len(query) < 2:
            raise HTTPException(status_code=400, detail="Query must be at least 2 characters long")
        
        suggestions = search_cities_with_suggestions(query, limit)
        return {"suggestions": suggestions}
    except Exception as e:
        logger.error(f"Error searching for cities: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to search for cities. Please try again."
        )


@router.get("/get-city-coordinates")
def get_city_coordinates(city_name: str = Query(..., description="City name"), country: str = Query(None, description="Optional country code")):
    """Get coordinates for a specific city."""
    try:
        coordinates = get_city_coordinates_with_rate_limit(city_name, country)
        if not coordinates:
            raise HTTPException(status_code=404, detail=f"City '{city_name}' not found")
        
        return coordinates
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting city coordinates: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get city coordinates. Please try again."
        )


@router.get("/calculate-sign/{birth_date}")
def calculate_zodiac_sign(birth_date: str):
    """Calculate zodiac sign from birth date."""
    try:
        sign = get_zodiac_sign(birth_date)
        if not sign:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid birth date format. Use YYYY-MM-DD or MM/DD/YYYY"
            )
        
        sign_info = get_sign_info(sign)
        return {
            "birth_date": birth_date,
            "zodiac_sign": sign,
            "sign_info": sign_info
        }
    except Exception as e:
        logger.error(f"Error calculating zodiac sign for {birth_date}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate zodiac sign. Please try again."
        )


@router.get("/sign-info/{sign}")
def get_sign_information(sign: str):
    """Get detailed information about a zodiac sign."""
    try:
        sign_info = get_sign_info(sign)
        if not sign_info:
            raise HTTPException(
                status_code=404,
                detail=f"Zodiac sign '{sign}' not found"
            )
        
        return {
            "sign": sign,
            "info": sign_info
        }
    except Exception as e:
        logger.error(f"Error getting sign info for {sign}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get sign information. Please try again."
        )


@router.get("/birth-chart")
def get_birth_chart(
    birth_date: str = Query(..., description="Birth date in YYYY-MM-DD format"),
    birth_time: str = Query(..., description="Birth time in HH:MM format (24-hour)"),
    latitude: float = Query(..., description="Birth location latitude"),
    longitude: float = Query(..., description="Birth location longitude")
):
    """Calculate birth chart for given birth data."""
    try:
        birth_chart = calculate_birth_chart(birth_date, birth_time, latitude, longitude)
        return birth_chart
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error calculating birth chart: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to calculate birth chart. Please try again."
        )


@router.get("/birth-chart/roast")
def get_birth_chart_roast(
    birth_date: str = Query(..., description="Birth date in YYYY-MM-DD format"),
    birth_time: str = Query(..., description="Birth time in HH:MM format (24-hour)"),
    latitude: float = Query(..., description="Birth location latitude"),
    longitude: float = Query(..., description="Birth location longitude")
):
    """Calculate birth chart and generate a roasted interpretation."""
    try:
        birth_chart = calculate_birth_chart(birth_date, birth_time, latitude, longitude)
        summary = generate_birth_chart_summary(birth_chart)
        roasted = roast_agent.run(summary)
        
        return {
            "birth_chart": birth_chart,
            "roast": roasted
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating birth chart roast: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate birth chart roast. Please try again."
        )


@router.get("/horoscope/{sign}")
def get_horoscope(sign: str, period: str = Query("daily", description="Time period: daily, yesterday, tomorrow, weekly, monthly")):
    """Get horoscope for a specific sign and time period."""
    valid_periods = ["daily", "yesterday", "tomorrow", "weekly", "monthly"]
    if period not in valid_periods:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid period. Must be one of: {', '.join(valid_periods)}"
        )
    
    try:
        cached = load_from_cache(sign, period)
        if cached is None:
            logger.info(f"Fetching fresh horoscope for {sign} ({period})")
            text = run_scraper(sign, period)
            save_to_cache(sign, period, text)
        else:
            logger.info(f"Using cached horoscope for {sign} ({period})")
            text = cached
        
        roasted = roast_agent.run(text)
        return {
            "sign": sign, 
            "period": period,
            "roast": roasted, 
            "source": "cached" if cached else "fresh"
        }
    except Exception as e:
        logger.error(f"Error processing horoscope for {sign} ({period}): {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to process horoscope for {sign}. Please try again later."
        )


@router.get("/horoscope/{sign}/daily")
def get_daily_horoscope(sign: str):
    """Legacy endpoint for daily horoscope - redirects to new endpoint."""
    return get_horoscope(sign, "daily")


@router.get("/horoscope/{sign}/yesterday")
def get_yesterday_horoscope(sign: str):
    """Get yesterday's horoscope for a sign."""
    return get_horoscope(sign, "yesterday")


@router.get("/horoscope/{sign}/tomorrow")
def get_tomorrow_horoscope(sign: str):
    """Get tomorrow's horoscope for a sign."""
    return get_horoscope(sign, "tomorrow")


@router.get("/horoscope/{sign}/weekly")
def get_weekly_horoscope(sign: str):
    """Get weekly horoscope for a sign."""
    return get_horoscope(sign, "weekly")


@router.get("/horoscope/{sign}/monthly")
def get_monthly_horoscope(sign: str):
    """Get monthly horoscope for a sign."""
    return get_horoscope(sign, "monthly")


@router.get("/sign/{sign}/description")
def get_sign_description(sign: str):
    try:
        cached = load_from_cache(sign, "description")
        if cached is None:
            logger.info(f"Fetching fresh description for {sign}")
            # Placeholder for future implementation
            description = run_scraper(sign, "daily")
            save_to_cache(sign, "description", description)
        else:
            logger.info(f"Using cached description for {sign}")
            description = cached
        
        roasted = roast_agent.run(description)
        return {"sign": sign, "personality": roasted, "source": "cached" if cached else "fresh"}
    except Exception as e:
        logger.error(f"Error processing description for {sign}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process description for {sign}. Please try again later."
        )
