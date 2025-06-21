import json
from pathlib import Path
from typing import Optional

CACHE_DIR = Path(__file__).resolve().parent.parent / ".." / "data" / "horoscopes"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def cache_path(sign: str, period: str) -> Path:
    return CACHE_DIR / f"{sign}_{period}.json"


def save_to_cache(sign: str, period: str, text: str) -> None:
    path = cache_path(sign, period)
    with path.open("w", encoding="utf-8") as f:
        json.dump({"text": text}, f)


def load_from_cache(sign: str, period: str) -> Optional[str]:
    path = cache_path(sign, period)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("text")
