"""
Birth chart calculator using ephem library.
"""
import ephem
from datetime import datetime
from typing import Dict, List, Optional
import logging
import math
import swisseph as swe

logger = logging.getLogger(__name__)

# Planetary symbols and names
PLANETS = {
    'Sun': '☉',
    'Moon': '☽',
    'Mercury': '☿',
    'Venus': '♀',
    'Mars': '♂',
    'Jupiter': '♃',
    'Saturn': '♄',
    'Uranus': '♅',
    'Neptune': '♆',
    'Pluto': '♇'
}

# Zodiac signs and their degrees
ZODIAC_SIGNS = [
    ('Aries', 0, 30, '♈'),
    ('Taurus', 30, 60, '♉'),
    ('Gemini', 60, 90, '♊'),
    ('Cancer', 90, 120, '♋'),
    ('Leo', 120, 150, '♌'),
    ('Virgo', 150, 180, '♍'),
    ('Libra', 180, 210, '♎'),
    ('Scorpio', 210, 240, '♏'),
    ('Sagittarius', 240, 270, '♐'),
    ('Capricorn', 270, 300, '♑'),
    ('Aquarius', 300, 330, '♒'),
    ('Pisces', 330, 360, '♓')
]

# Houses and their meanings
HOUSES = {
    1: "Self, personality, appearance",
    2: "Money, possessions, values",
    3: "Communication, siblings, short trips",
    4: "Home, family, roots",
    5: "Creativity, romance, children",
    6: "Work, health, daily routine",
    7: "Partnerships, marriage, open enemies",
    8: "Transformation, shared resources, death",
    9: "Higher education, travel, philosophy",
    10: "Career, public image, authority",
    11: "Friends, groups, hopes and dreams",
    12: "Spirituality, hidden things, subconscious"
}


def get_zodiac_sign(degrees: float) -> Dict[str, str]:
    """Get zodiac sign for given degrees."""
    for sign_name, start_deg, end_deg, symbol in ZODIAC_SIGNS:
        if start_deg <= degrees < end_deg:
            return {
                'name': sign_name,
                'symbol': symbol,
                'degrees': degrees,
                'sign_degrees': degrees - start_deg
            }
    # Handle edge case for 360 degrees
    return {
        'name': 'Aries',
        'symbol': '♈',
        'degrees': degrees,
        'sign_degrees': 0
    }


def format_degrees(degrees: float) -> str:
    """Format degrees in zodiac notation."""
    sign_data = get_zodiac_sign(degrees)
    return f"{sign_data['sign_degrees']:.1f}° {sign_data['name']}"


def get_julian_day(birth_date: str, birth_time: str) -> float:
    dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)


def calculate_ascendant_midheaven_swe(birth_date: str, birth_time: str, latitude: float, longitude: float) -> tuple:
    """
    Use Swiss Ephemeris to calculate Ascendant and MC (Midheaven).
    Returns (ascendant_degrees, mc_degrees)
    """
    jd = get_julian_day(birth_date, birth_time)
    # 'P' = Placidus houses (default)
    # Returns: cusps, ascmc (ascendant, MC, ARMC, Vertex, Equatorial Ascendant, Co-Ascendant, Polar Ascendant)
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    asc = ascmc[0]  # Ascendant
    mc = ascmc[1]   # Midheaven
    return asc, mc


def calculate_birth_chart(birth_date: str, birth_time: str, latitude: float, longitude: float) -> Dict:
    """
    Calculate birth chart for given birth data.
    Uses ephem for planets, Swiss Ephemeris for Ascendant/MC and houses.
    """
    try:
        # Parse date and time
        datetime_str = f"{birth_date} {birth_time}"
        birth_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        
        # Get Julian Day for Swiss Ephemeris
        jd = get_julian_day(birth_date, birth_time)
        
        # Calculate house cusps using Placidus system
        cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')

        # Function to find which house a planet is in
        def get_planet_house(planet_degrees: float) -> int:
            """Determines the house placement of a celestial body."""
            # Normalize degrees to be within the 0-360 range
            planet_degrees = planet_degrees % 360
            cusps_12 = list(cusps[:12])
            for i in range(12):
                start_cusp = cusps_12[i]
                end_cusp = cusps_12[(i + 1) % 12]
                # Handles the wrap-around from the 12th to the 1st house (e.g., 330° to 20°)
                if start_cusp > end_cusp:
                    if planet_degrees >= start_cusp or planet_degrees < end_cusp:
                        return i + 1
                # Standard case
                elif start_cusp <= planet_degrees < end_cusp:
                    return i + 1
            return 12 # Default to 12th house if no match is found

        # Create observer (birth location) for ephem
        observer = ephem.Observer()
        observer.lat = str(latitude)
        observer.lon = str(longitude)
        observer.date = birth_datetime
        
        # Calculate planetary positions
        planets_data = {}
        for planet_name in PLANETS.keys():
            try:
                if planet_name == 'Sun':
                    planet = ephem.Sun()
                elif planet_name == 'Moon':
                    planet = ephem.Moon()
                elif planet_name == 'Mercury':
                    planet = ephem.Mercury()
                elif planet_name == 'Venus':
                    planet = ephem.Venus()
                elif planet_name == 'Mars':
                    planet = ephem.Mars()
                elif planet_name == 'Jupiter':
                    planet = ephem.Jupiter()
                elif planet_name == 'Saturn':
                    planet = ephem.Saturn()
                elif planet_name == 'Uranus':
                    planet = ephem.Uranus()
                elif planet_name == 'Neptune':
                    planet = ephem.Neptune()
                elif planet_name == 'Pluto':
                    planet = ephem.Pluto()
                else:
                    continue
                planet.compute(observer)
                degrees = float(planet.hlong) * 180 / ephem.pi
                sign_data = get_zodiac_sign(degrees)
                house = get_planet_house(degrees)
                
                planets_data[planet_name] = {
                    'name': planet_name,
                    'symbol': PLANETS[planet_name],
                    'degrees': degrees,
                    'sign': sign_data['name'],
                    'sign_symbol': sign_data['symbol'],
                    'sign_degrees': sign_data['sign_degrees'],
                    'formatted': format_degrees(degrees),
                    'house': house
                }
            except Exception as e:
                logger.warning(f"Failed to calculate {planet_name}: {e}")
                continue
        
        # Use Swiss Ephemeris for Ascendant and MC
        asc_degrees, mc_degrees = ascmc[0], ascmc[1]
        asc_sign_data = get_zodiac_sign(asc_degrees)
        ascendant = {
            'name': 'Ascendant',
            'symbol': 'AC',
            'degrees': asc_degrees,
            'sign': asc_sign_data['name'],
            'sign_symbol': asc_sign_data['symbol'],
            'sign_degrees': asc_sign_data['sign_degrees'],
            'formatted': format_degrees(asc_degrees)
        }
        mc_sign_data = get_zodiac_sign(mc_degrees)
        midheaven = {
            'name': 'Midheaven',
            'symbol': 'MC',
            'degrees': mc_degrees,
            'sign': mc_sign_data['name'],
            'sign_symbol': mc_sign_data['symbol'],
            'sign_degrees': mc_sign_data['sign_degrees'],
            'formatted': format_degrees(mc_degrees)
        }
        
        # House cusps data
        house_cusps_data = {}
        for i, cusp_degrees in enumerate(cusps[:12]):
            sign_data = get_zodiac_sign(cusp_degrees)
            house_cusps_data[i+1] = {
                'house': i + 1,
                'degrees': cusp_degrees,
                'sign': sign_data['name'],
                'sign_symbol': sign_data['symbol'],
                'formatted': format_degrees(cusp_degrees)
            }

        return {
            'birth_data': {
                'date': birth_date,
                'time': birth_time,
                'datetime': birth_datetime.isoformat(),
                'latitude': latitude,
                'longitude': longitude
            },
            'planets': planets_data,
            'ascendant': ascendant,
            'midheaven': midheaven,
            'houses': house_cusps_data,
            'calculated_at': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to calculate birth chart: {e}")
        raise ValueError(f"Invalid birth data: {e}")


def get_planet_interpretation(planet: str, sign: str) -> str:
    """Get basic interpretation for planet in sign."""
    interpretations = {
        'Sun': {
            'Aries': 'Bold, energetic, and natural leader',
            'Taurus': 'Stable, determined, and practical',
            'Gemini': 'Versatile, curious, and communicative',
            'Cancer': 'Emotional, nurturing, and protective',
            'Leo': 'Charismatic, generous, and dramatic',
            'Virgo': 'Analytical, practical, and perfectionist',
            'Libra': 'Diplomatic, fair, and relationship-oriented',
            'Scorpio': 'Intense, passionate, and mysterious',
            'Sagittarius': 'Optimistic, adventurous, and philosophical',
            'Capricorn': 'Ambitious, disciplined, and responsible',
            'Aquarius': 'Original, independent, and humanitarian',
            'Pisces': 'Compassionate, artistic, and intuitive'
        },
        'Moon': {
            'Aries': 'Emotionally impulsive and quick to react',
            'Taurus': 'Emotionally stable and security-seeking',
            'Gemini': 'Emotionally curious and changeable',
            'Cancer': 'Deeply emotional and nurturing',
            'Leo': 'Emotionally expressive and dramatic',
            'Virgo': 'Emotionally analytical and practical',
            'Libra': 'Emotionally balanced and relationship-focused',
            'Scorpio': 'Emotionally intense and transformative',
            'Sagittarius': 'Emotionally optimistic and adventurous',
            'Capricorn': 'Emotionally reserved and responsible',
            'Aquarius': 'Emotionally independent and unconventional',
            'Pisces': 'Emotionally sensitive and compassionate'
        }
    }
    
    return interpretations.get(planet, {}).get(sign, f"{planet} in {sign} indicates unique personality traits")


def generate_birth_chart_summary(birth_chart: Dict) -> str:
    """Generate a summary of the birth chart for roasting."""
    planets = birth_chart.get('planets', {})
    
    if not planets:
        return "Unable to calculate birth chart - the stars are as confused as your life choices."
    
    # Get key placements
    sun_sign = planets.get('Sun', {}).get('sign', 'Unknown')
    moon_sign = planets.get('Moon', {}).get('sign', 'Unknown')
    ascendant = birth_chart.get('ascendant', {}).get('sign', 'Unknown')
    
    summary = f"Your birth chart shows a Sun in {sun_sign}, Moon in {moon_sign}, and Rising sign in {ascendant}. "
    
    # Add some planetary aspects
    aspects = []
    for planet_name, planet_data in planets.items():
        if planet_name in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars']:
            sign = planet_data.get('sign', 'Unknown')
            aspects.append(f"{planet_name} in {sign}")
    
    if aspects:
        summary += f"Key placements include: {', '.join(aspects)}. "
    
    summary += "This cosmic fingerprint reveals the unique blend of energies that make you... well, you."
    
    return summary 