import logging
import requests
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from backend.agents.scraper_agent.agent import run_scraper
from backend.agents.roast_agent import agent as roast_agent
from backend.agents.roast_agent.agent import run_birth_chart_synthesis
from backend.api.utils.caching import load_from_cache, save_to_cache
from backend.core.zodiac_calculator import get_zodiac_sign, get_sign_info
from backend.core.birth_chart_calculator import calculate_birth_chart, generate_birth_chart_summary, ZODIAC_SIGNS
from backend.core.geocoder import search_cities_with_suggestions, get_city_coordinates_with_rate_limit
from itertools import combinations
import json
import asyncio
from typing import AsyncGenerator

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


@router.get("/birth-chart/roast-placements")
async def get_birth_chart_placement_roasts(
    birth_date: str = Query(..., description="Birth date in YYYY-MM-DD format"),
    birth_time: str = Query(..., description="Birth time in HH:MM format (24-hour)"),
    latitude: float = Query(..., description="Birth location latitude"),
    longitude: float = Query(..., description="Birth location longitude"),
    language: str = Query("English", description="Language for roasts (English, French, Russian)")
):
    """Calculate birth chart and generate a roasted interpretation for each planetary placement."""
    try:
        birth_chart = calculate_birth_chart(birth_date, birth_time, latitude, longitude)
        placements = birth_chart.get('planets', {})
        
        async def generate_roasts() -> AsyncGenerator[str, None]:
            """Stream roasts as they're generated."""
            placement_roasts = {}
            
            for planet, data in placements.items():
                try:
                    # Construct a detailed prompt for the agent
                    prompt = (
                        f"Generate a witty, insightful, and slightly sarcastic astrological roast "
                        f"for a person with {data['name']} in {data['sign']} in the {data['house']}th house. "
                        f"Focus on the unique combination of this planet, sign, and house."
                    )
                    
                    # Run the agent to get the roast with language parameter
                    roast = roast_agent.run(prompt, language)
                    placement_roasts[planet] = roast
                    
                    # Stream the current planet's roast
                    yield f"data: {json.dumps({'planet': planet, 'roast': roast, 'complete': False})}\n\n"
                    
                    # Small delay to make streaming visible
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Failed to generate roast for {planet}: {e}")
                    placement_roasts[planet] = "Couldn't generate a roast for this placement. It's probably too basic."
                    yield f"data: {json.dumps({'planet': planet, 'roast': placement_roasts[planet], 'complete': False})}\n\n"
            
            # Generate synthesis roast after all planet roasts are complete
            try:
                synthesis = run_birth_chart_synthesis(placement_roasts, language)
                placement_roasts['overall_synthesis'] = synthesis
                
                # Stream the synthesis
                yield f"data: {json.dumps({'planet': 'overall_synthesis', 'roast': synthesis, 'complete': False})}\n\n"
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Failed to generate synthesis: {e}")
                synthesis = "Your cosmic blueprint is so complex that even our advanced AI gave up trying to synthesize it into one coherent roast."
                placement_roasts['overall_synthesis'] = synthesis
                yield f"data: {json.dumps({'planet': 'overall_synthesis', 'roast': synthesis, 'complete': False})}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'complete': True, 'all_roasts': placement_roasts})}\n\n"
        
        return StreamingResponse(
            generate_roasts(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating placement roasts: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate placement roasts. Please try again."
        )


@router.get("/birth-chart/plot")
def plot_birth_chart(
    birth_date: str = Query(..., description="Birth date in YYYY-MM-DD format"),
    birth_time: str = Query(..., description="Birth time in HH:MM format (24-hour)"),
    latitude: float = Query(..., description="Birth location latitude"),
    longitude: float = Query(..., description="Birth location longitude")
):
    """Generate and return a PNG image of the birth chart wheel in a minimalistic style."""
    try:
        chart = calculate_birth_chart(birth_date, birth_time, latitude, longitude)
        planets = chart['planets']
        asc = chart['ascendant']
        mc = chart['midheaven']
        
        all_points = {**planets, 'Ascendant': asc, 'Midheaven': mc}

        # --- Chart Styling ---
        fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': 'polar'})
        ax.set_theta_offset(np.pi)  # Set 0 degrees (Aries) to the left
        ax.set_theta_direction(1) # Ensure Counter-Clockwise
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['polar'].set_visible(False)
        ax.set_facecolor('#FFFFFF')
        fig.patch.set_facecolor('#FFFFFF')

        def tangent_rotation(screen_theta_rad: float) -> float:
            """
            Returns a text rotation (deg) that keeps the label tangential
            to the ring *and* upright, using the final screen angle.
            """
            deg = np.degrees(screen_theta_rad) % 360
            rot = deg - 90
            # Flip text on the bottom half of the screen (180 to 360 degrees)
            if 180 < deg < 360:
                rot += 180
            return rot % 360

        # --- Draw Rings ---
        ax.fill_between(np.linspace(0, 2 * np.pi, 200), 1.0, 1.2, color='black', zorder=2)
        ax.fill_between(np.linspace(0, 2 * np.pi, 200), 0.8, 1.0, color='#F0F0F0', zorder=1)
        ax.fill_between(np.linspace(0, 2 * np.pi, 200), 0, 0.8, color='white', zorder=1)
        
        # --- Degree Markers ---
        for i in range(360):
            angle = np.deg2rad(i)
            style = {'color': '#AAAAAA', 'lw': 0.5, 'zorder': 3}
            if i % 10 == 0:
                ax.plot([angle, angle], [0.97, 1.0], **style)
            elif i % 5 == 0:
                ax.plot([angle, angle], [0.98, 1.0], **style)
            else:
                ax.plot([angle, angle], [0.99, 1.0], **style)

        # --- Zodiac Signs and Separators ---
        for i in range(12):
            angle_deg_start = i * 30
            angle_rad_start = np.deg2rad(angle_deg_start)
            ax.plot([angle_rad_start, angle_rad_start], [1.0, 1.2], color='white', lw=1.5, zorder=3)
            
            sign_name = ZODIAC_SIGNS[i][0].upper()
            data_theta_rad = np.deg2rad(angle_deg_start + 15)
            
            # Calculate the final screen angle by applying the offset
            screen_theta_rad = data_theta_rad + ax.get_theta_offset()

            ax.text(
                data_theta_rad, # Position is in data coordinates
                1.1,
                sign_name,
                ha='center',
                va='center',
                fontsize=11,
                fontweight='bold',
                color='white',
                rotation=tangent_rotation(screen_theta_rad), # Rotation is based on the final screen angle
                rotation_mode='anchor',
                zorder=4
            )

        # --- Plot Planets & Points ---
        for name, data in all_points.items():
            angle = np.deg2rad(data['degrees'])
            radius = 0.9 if name not in ['Ascendant', 'Midheaven'] else 1.0
            symbol = data['symbol']
            
            # Use specific symbols for AC/MC
            if name == 'Ascendant':
                symbol = 'AC'
            elif name == 'Midheaven':
                symbol = 'MC'
                
            ax.text(angle, radius, symbol, ha='center', va='center', fontsize=16 if name in ['Ascendant', 'Midheaven'] else 14, 
                    color='black', zorder=5, bbox=dict(boxstyle='circle,pad=0.2', fc='white', ec='none'))
            
            # Planet degree labels
            if name not in ['Ascendant', 'Midheaven']:
                 ax.text(angle, 0.82, f"{data['sign_degrees']:.0f}°", ha='center', va='center', fontsize=8, color='#555', zorder=5)

        # --- Calculate and Draw Aspects ---
        ASPECTS = {
            'Conjunction': (0, 8, 'solid', 1.0),
            'Opposition': (180, 8, 'solid', 1.0),
            'Trine': (120, 7, 'solid', 0.8),
            'Square': (90, 7, 'dashed', 0.8),
            'Sextile': (60, 5, 'dashed', 0.6),
        }
        
        # Only use planets for aspects, not AC/MC
        aspect_points = list(planets.values())
        
        for p1, p2 in combinations(aspect_points, 2):
            angle_diff = abs(p1['degrees'] - p2['degrees'])
            angle_diff = min(angle_diff, 360 - angle_diff)

            for name, (deg, orb, style, alpha) in ASPECTS.items():
                if abs(angle_diff - deg) <= orb:
                    angle1 = np.deg2rad(p1['degrees'])
                    angle2 = np.deg2rad(p2['degrees'])
                    ax.plot([angle1, angle2], [0.8, 0.8], color='#AAAAAA', ls=style, lw=0.8, zorder=1, alpha=alpha)
                    break
                    
        # Final adjustments
        ax.set_ylim(0, 1.2)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor=fig.get_facecolor())
        plt.close(fig)
        buf.seek(0)
        return StreamingResponse(buf, media_type='image/png')
        
    except Exception as e:
        logger.error(f"Error generating new chart plot: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to generate chart image.")


@router.get("/horoscope/{sign}")
def get_horoscope(sign: str, period: str = Query("daily", description="Time period: daily, yesterday, tomorrow, weekly, monthly"), language: str = Query("English", description="Language for roasts (English, French, Russian)")):
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
        
        roasted = roast_agent.run_categorized(text, language)
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
def get_sign_description(sign: str, language: str = Query("English", description="Language for roasts (English, French, Russian)")):
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
        
        roasted = roast_agent.run(description, language)
        return {"sign": sign, "personality": roasted, "source": "cached" if cached else "fresh"}
    except Exception as e:
        logger.error(f"Error processing description for {sign}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process description for {sign}. Please try again later."
        )
