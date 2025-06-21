"""
Geocoding utility using Nominatim API (OpenStreetMap).
"""
import requests
import logging
from typing import Dict, Optional, List
import time

logger = logging.getLogger(__name__)

# Nominatim API base URL
NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/search"

# User agent for API requests (required by Nominatim)
USER_AGENT = "HoroscHope/1.0 (https://github.com/your-repo/horosc-hope)"


def search_city(city_name: str, country: str = None) -> List[Dict]:
    """
    Search for a city and return possible matches.
    
    Args:
        city_name: Name of the city to search for
        country: Optional country code to narrow search
    
    Returns:
        List of matching locations with coordinates
    """
    try:
        # Build search query
        query = city_name
        if country:
            query += f", {country}"
        
        params = {
            'q': query,
            'format': 'json',
            'limit': 10,  # Get top 10 results
            'addressdetails': 1,
            'accept-language': 'en'
        }
        
        headers = {
            'User-Agent': USER_AGENT
        }
        
        logger.info(f"Searching for city: {query}")
        
        response = requests.get(
            NOMINATIM_BASE_URL,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        results = response.json()
        
        # Filter and format results
        formatted_results = []
        for result in results:
            if result.get('lat') and result.get('lon'):
                formatted_results.append({
                    'name': result.get('display_name', ''),
                    'latitude': float(result['lat']),
                    'longitude': float(result['lon']),
                    'type': result.get('type', ''),
                    'importance': result.get('importance', 0),
                    'country': result.get('address', {}).get('country', ''),
                    'state': result.get('address', {}).get('state', ''),
                    'city': result.get('address', {}).get('city', '') or result.get('address', {}).get('town', '')
                })
        
        # Sort by importance (higher importance = more relevant)
        formatted_results.sort(key=lambda x: x['importance'], reverse=True)
        
        logger.info(f"Found {len(formatted_results)} results for {city_name}")
        return formatted_results
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching for city {city_name}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error searching for city {city_name}: {e}")
        return []


def get_city_coordinates(city_name: str, country: str = None) -> Optional[Dict]:
    """
    Get coordinates for a specific city.
    
    Args:
        city_name: Name of the city
        country: Optional country code to narrow search
    
    Returns:
        Dictionary with latitude and longitude, or None if not found
    """
    results = search_city(city_name, country)
    
    if not results:
        return None
    
    # Return the most relevant result (highest importance)
    best_match = results[0]
    
    return {
        'latitude': best_match['latitude'],
        'longitude': best_match['longitude'],
        'name': best_match['name'],
        'country': best_match['country'],
        'state': best_match['state']
    }


def search_cities_with_suggestions(query: str, limit: int = 5) -> List[Dict]:
    """
    Search for cities and return suggestions for autocomplete.
    
    Args:
        query: Partial city name to search for
        limit: Maximum number of suggestions to return
    
    Returns:
        List of city suggestions
    """
    try:
        params = {
            'q': query,
            'format': 'json',
            'limit': limit,
            'addressdetails': 1,
            'accept-language': 'en',
            'featuretype': 'city'  # Focus on cities
        }
        
        headers = {
            'User-Agent': USER_AGENT
        }
        
        response = requests.get(
            NOMINATIM_BASE_URL,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        results = response.json()
        
        suggestions = []
        for result in results:
            if result.get('lat') and result.get('lon'):
                address = result.get('address', {})
                city_name = address.get('city', '') or address.get('town', '') or address.get('village', '')
                country = address.get('country', '')
                state = address.get('state', '')
                
                if city_name:
                    display_name = f"{city_name}"
                    if state:
                        display_name += f", {state}"
                    if country:
                        display_name += f", {country}"
                    
                    suggestions.append({
                        'display_name': display_name,
                        'city': city_name,
                        'state': state,
                        'country': country,
                        'latitude': float(result['lat']),
                        'longitude': float(result['lon'])
                    })
        
        return suggestions
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching for city suggestions: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error searching for city suggestions: {e}")
        return []


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate that coordinates are within reasonable bounds.
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
    
    Returns:
        True if coordinates are valid, False otherwise
    """
    return (
        -90 <= latitude <= 90 and
        -180 <= longitude <= 180
    )


# Rate limiting helper (Nominatim has usage limits)
class RateLimiter:
    def __init__(self, max_requests_per_second: float = 1.0):
        self.max_requests_per_second = max_requests_per_second
        self.last_request_time = 0
    
    def wait_if_needed(self):
        """Wait if necessary to respect rate limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_interval = 1.0 / self.max_requests_per_second
        
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests_per_second=1.0)


def search_city_with_rate_limit(city_name: str, country: str = None) -> List[Dict]:
    """Search for city with rate limiting."""
    rate_limiter.wait_if_needed()
    return search_city(city_name, country)


def get_city_coordinates_with_rate_limit(city_name: str, country: str = None) -> Optional[Dict]:
    """Get city coordinates with rate limiting."""
    rate_limiter.wait_if_needed()
    return get_city_coordinates(city_name, country) 