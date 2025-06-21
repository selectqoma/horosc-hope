"""
Zodiac sign calculator based on date of birth.
"""
from datetime import datetime
from typing import Optional


def get_zodiac_sign(birth_date: str) -> Optional[str]:
    """
    Calculate zodiac sign based on date of birth.
    
    Args:
        birth_date: Date string in format 'YYYY-MM-DD' or 'MM/DD/YYYY'
    
    Returns:
        Zodiac sign in lowercase, or None if invalid date
    """
    try:
        # Try different date formats
        if '-' in birth_date:
            date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
        elif '/' in birth_date:
            date_obj = datetime.strptime(birth_date, '%m/%d/%Y')
        else:
            return None
        
        month = date_obj.month
        day = date_obj.day
        
        return _calculate_sign(month, day)
        
    except ValueError:
        return None


def _calculate_sign(month: int, day: int) -> str:
    """
    Calculate zodiac sign based on month and day.
    
    Args:
        month: Month (1-12)
        day: Day (1-31)
    
    Returns:
        Zodiac sign in lowercase
    """
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "aquarius"
    else:  # (month == 2 and day >= 19) or (month == 3 and day <= 20)
        return "pisces"


def get_sign_info(sign: str) -> dict:
    """
    Get information about a zodiac sign.
    
    Args:
        sign: Zodiac sign in lowercase
    
    Returns:
        Dictionary with sign information
    """
    sign_info = {
        "aries": {
            "name": "Aries",
            "element": "Fire",
            "quality": "Cardinal",
            "ruler": "Mars",
            "dates": "March 21 - April 19",
            "traits": ["Courageous", "Energetic", "Willful", "Pioneering", "Independent"]
        },
        "taurus": {
            "name": "Taurus",
            "element": "Earth",
            "quality": "Fixed",
            "ruler": "Venus",
            "dates": "April 20 - May 20",
            "traits": ["Patient", "Reliable", "Devoted", "Persistent", "Determined"]
        },
        "gemini": {
            "name": "Gemini",
            "element": "Air",
            "quality": "Mutable",
            "ruler": "Mercury",
            "dates": "May 21 - June 20",
            "traits": ["Adaptable", "Versatile", "Communicative", "Witty", "Intellectual"]
        },
        "cancer": {
            "name": "Cancer",
            "element": "Water",
            "quality": "Cardinal",
            "ruler": "Moon",
            "dates": "June 21 - July 22",
            "traits": ["Nurturing", "Protective", "Sympathetic", "Moody", "Homebody"]
        },
        "leo": {
            "name": "Leo",
            "element": "Fire",
            "quality": "Fixed",
            "ruler": "Sun",
            "dates": "July 23 - August 22",
            "traits": ["Creative", "Passionate", "Generous", "Warm-hearted", "Cheerful"]
        },
        "virgo": {
            "name": "Virgo",
            "element": "Earth",
            "quality": "Mutable",
            "ruler": "Mercury",
            "dates": "August 23 - September 22",
            "traits": ["Loyal", "Analytical", "Kind", "Hardworking", "Practical"]
        },
        "libra": {
            "name": "Libra",
            "element": "Air",
            "quality": "Cardinal",
            "ruler": "Venus",
            "dates": "September 23 - October 22",
            "traits": ["Diplomatic", "Gracious", "Fair-minded", "Peaceful", "Idealistic"]
        },
        "scorpio": {
            "name": "Scorpio",
            "element": "Water",
            "quality": "Fixed",
            "ruler": "Pluto",
            "dates": "October 23 - November 21",
            "traits": ["Passionate", "Stubborn", "Resourceful", "Brave", "A true friend"]
        },
        "sagittarius": {
            "name": "Sagittarius",
            "element": "Fire",
            "quality": "Mutable",
            "ruler": "Jupiter",
            "dates": "November 22 - December 21",
            "traits": ["Optimistic", "Loves freedom", "Jovial", "Good-humored", "Honest"]
        },
        "capricorn": {
            "name": "Capricorn",
            "element": "Earth",
            "quality": "Cardinal",
            "ruler": "Saturn",
            "dates": "December 22 - January 19",
            "traits": ["Responsible", "Disciplined", "Self-controlled", "Good managers"]
        },
        "aquarius": {
            "name": "Aquarius",
            "element": "Air",
            "quality": "Fixed",
            "ruler": "Uranus",
            "dates": "January 20 - February 18",
            "traits": ["Progressive", "Original", "Independent", "Humanitarian"]
        },
        "pisces": {
            "name": "Pisces",
            "element": "Water",
            "quality": "Mutable",
            "ruler": "Neptune",
            "dates": "February 19 - March 20",
            "traits": ["Compassionate", "Artistic", "Intuitive", "Gentle", "Wise"]
        }
    }
    
    return sign_info.get(sign.lower(), {}) 