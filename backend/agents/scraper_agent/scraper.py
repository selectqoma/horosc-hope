import requests
from bs4 import BeautifulSoup
from typing import Dict


def fetch_horoscopes(sign: str, period: str = "daily") -> Dict[str, str]:
    """Fetch horoscope text from the Aztro API."""
    day_map = {
        "daily": "today",
        "yesterday": "yesterday",
        "tomorrow": "tomorrow",
    }
    day = day_map.get(period, "today")
    url = "https://aztro.sameerkumar.website/"  # public API
    response = requests.post(url, params={"sign": sign, "day": day})
    response.raise_for_status()
    data = response.json()
    return {period: data.get("description", "")}


def normalize(text: str) -> str:
    """Simple HTML stripping and whitespace normalization."""
    soup = BeautifulSoup(text, "html.parser")
    cleaned = soup.get_text(separator=" ")
    return " ".join(cleaned.split())
