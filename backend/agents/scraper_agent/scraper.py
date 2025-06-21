import requests
import logging
import random
from bs4 import BeautifulSoup
from typing import Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_horoscopes(sign: str, period: str = "daily") -> Dict[str, str]:
    """Fetch horoscope text from horoscope-app-api.vercel.app with fallback."""
    # Capitalize the sign as required by the API
    sign_cap = sign.capitalize()
    base_url = "https://horoscope-app-api.vercel.app/api/v1"
    try:
        if period in ["daily", "yesterday", "tomorrow"]:
            day_map = {
                "daily": "TODAY",
                "yesterday": "YESTERDAY",
                "tomorrow": "TOMORROW"
            }
            day = day_map.get(period, "TODAY")
            url = f"{base_url}/get-horoscope/daily"
            params = {"sign": sign_cap, "day": day}
        elif period == "weekly":
            url = f"{base_url}/get-horoscope/weekly"
            params = {"sign": sign_cap}
        elif period == "monthly":
            url = f"{base_url}/get-horoscope/monthly"
            params = {"sign": sign_cap}
        else:
            # Default to daily if unknown period
            url = f"{base_url}/get-horoscope/daily"
            params = {"sign": sign_cap, "day": "TODAY"}
        logger.info(f"Fetching horoscope for {sign_cap} ({period}) from horoscope-app-api.vercel.app")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse the actual API response format
        if isinstance(data, dict) and data.get("success") and "data" in data:
            horoscope_data = data["data"]
            if isinstance(horoscope_data, dict):
                text = horoscope_data.get("horoscope_data") or horoscope_data.get("horoscope") or horoscope_data.get("description")
                if text:
                    logger.info(f"Successfully fetched from horoscope-app-api.vercel.app")
                    return {period: text}
        
        logger.warning(f"Unexpected API response format: {data}")
    except Exception as e:
        logger.warning(f"Failed to fetch from horoscope-app-api.vercel.app: {e}")
    # Use local generation as fallback
    logger.info(f"Using local generation for {sign} ({period})")
    return {period: generate_local_horoscope(sign, period)}


def generate_local_horoscope(sign: str, period: str) -> str:
    """Generate a varied horoscope locally based on sign and period."""
    
    # Base personality traits for each sign
    sign_traits = {
        "aries": ["fiery", "energetic", "impulsive", "courageous", "adventurous"],
        "taurus": ["stubborn", "patient", "reliable", "practical", "determined"],
        "gemini": ["versatile", "curious", "communicative", "adaptable", "witty"],
        "cancer": ["emotional", "nurturing", "intuitive", "protective", "sensitive"],
        "leo": ["charismatic", "generous", "proud", "creative", "dramatic"],
        "virgo": ["analytical", "practical", "diligent", "modest", "intelligent"],
        "libra": ["diplomatic", "gracious", "fair", "peaceful", "indecisive"],
        "scorpio": ["passionate", "mysterious", "intense", "loyal", "strategic"],
        "sagittarius": ["optimistic", "adventurous", "honest", "philosophical", "independent"],
        "capricorn": ["responsible", "disciplined", "ambitious", "patient", "practical"],
        "aquarius": ["original", "independent", "humanitarian", "intellectual", "unconventional"],
        "pisces": ["compassionate", "artistic", "intuitive", "gentle", "dreamy"]
    }
    
    # Daily themes and activities
    themes = [
        "communication", "work", "relationships", "health", "creativity", 
        "finance", "travel", "learning", "spirituality", "social life"
    ]
    
    # Mood variations
    moods = [
        "feeling particularly inspired", "a bit overwhelmed", "surprisingly calm", 
        "extra motivated", "slightly confused", "very focused", "somewhat distracted",
        "incredibly productive", "a little restless", "deeply contemplative"
    ]
    
    # Action suggestions
    actions = [
        "take a moment to breathe", "trust your instincts", "step out of your comfort zone",
        "listen to your inner voice", "embrace the unexpected", "focus on what matters most",
        "let go of what you can't control", "celebrate your achievements", 
        "connect with loved ones", "pursue your passions"
    ]
    
    # Get sign-specific traits
    traits = sign_traits.get(sign.lower(), ["unique", "special", "interesting"])
    trait = random.choice(traits)
    theme = random.choice(themes)
    mood = random.choice(moods)
    action = random.choice(actions)
    
    # Generate period-specific content
    if period == "yesterday":
        return f"Yesterday, your {trait} nature was {mood}. The stars aligned around {theme}, and you should {action}. Remember, every day is a new opportunity to shine!"
    elif period == "tomorrow":
        return f"Tomorrow, your {trait} energy will be {mood}. The universe is focusing on {theme}, so prepare to {action}. Trust that the cosmos has your back!"
    elif period == "weekly":
        return f"This week, your {trait} qualities will be {mood}. The stars are shining on {theme}, so it's a great time to {action}."
    elif period == "monthly":
        return f"This month, your {trait} side is {mood}. The universe is highlighting {theme}, so make sure to {action}."
    else:  # daily/today
        return f"Today, your {trait} spirit is {mood}. The celestial energies are highlighting {theme}, making it the perfect time to {action}. Your unique cosmic fingerprint is guiding you toward something special."


def get_fallback_horoscope(sign: str, period: str) -> str:
    """Legacy fallback horoscope - now using the new generation system."""
    return generate_local_horoscope(sign, period)


def normalize(text: str) -> str:
    """Simple HTML stripping and whitespace normalization."""
    soup = BeautifulSoup(text, "html.parser")
    cleaned = soup.get_text(separator=" ")
    return " ".join(cleaned.split())
