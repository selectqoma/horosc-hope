from .scraper import fetch_horoscopes, normalize


def run_scraper(sign: str, period: str = "daily") -> str:
    """Fetch, normalize, and cache horoscope data."""
    raw = fetch_horoscopes(sign, period)
    text = raw.get(period, "")
    cleaned = normalize(text)
    return cleaned
