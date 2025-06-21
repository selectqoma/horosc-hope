from .scraper import fetch_horoscopes, normalize


def run_scraper(sign: str, period: str = "daily") -> str:
    """Fetch, normalize, and cache horoscope data."""
    raw = fetch_horoscopes(sign, period)
    text = raw.get(period, "")
    if not text:
        # If no text was returned, use fallback
        from .scraper import get_fallback_horoscope
        text = get_fallback_horoscope(sign, period)
    cleaned = normalize(text)
    return cleaned
