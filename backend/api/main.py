import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.horoscope import router as horoscope_router
from ..agents.scraper_agent.agent import run_scraper
from .utils.caching import save_to_cache
from ..core.daily_data_manager import load_daily_horoscopes, save_daily_horoscopes, is_data_fresh, cleanup_old_data
import logging

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="HoroscHope API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(horoscope_router)

# List of all zodiac signs
ALL_SIGNS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]
ALL_PERIODS = ["daily", "yesterday", "tomorrow"]

@app.on_event("startup")
def prefetch_horoscopes():
    logger = logging.getLogger("startup")
    logger.info("Starting horoscope data initialization...")
    
    # Clean up old data first
    cleanup_old_data()
    
    # Check if we have fresh data for today
    if is_data_fresh():
        logger.info("Found fresh daily horoscope data, loading from disk...")
        daily_data = load_daily_horoscopes()
        if daily_data:
            # Load the data into cache
            for sign, periods in daily_data.items():
                for period, text in periods.items():
                    save_to_cache(sign, period, text)
            logger.info("Successfully loaded daily horoscopes from disk")
            return
    
    # If no fresh data, fetch from API and save to disk
    logger.info("No fresh data found, fetching horoscopes from API...")
    all_horoscopes = {}
    
    for sign in ALL_SIGNS:
        all_horoscopes[sign] = {}
        for period in ALL_PERIODS:
            try:
                text = run_scraper(sign, period)
                save_to_cache(sign, period, text)
                all_horoscopes[sign][period] = text
                logger.info(f"Cached {sign} ({period})")
            except Exception as e:
                logger.error(f"Failed to cache {sign} ({period}): {e}")
    
    # Save all horoscopes to disk
    save_daily_horoscopes(all_horoscopes)
    logger.info("Pre-fetching complete and saved to disk.")

@app.get("/")
def read_root():
    return {"message": "HoroscHope API"}
