"""
Daily data manager for saving and loading horoscope data.
"""
import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "daily_horoscopes"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Valid time periods
VALID_PERIODS = ["daily", "yesterday", "tomorrow", "weekly", "monthly"]


def get_today_filename() -> str:
    """Get filename for today's data."""
    today = date.today()
    return f"horoscopes_{today.strftime('%Y-%m-%d')}.json"


def get_data_file_path() -> Path:
    """Get the path to today's data file."""
    return DATA_DIR / get_today_filename()


def save_horoscopes(horoscopes: Dict[str, Dict[str, str]], period: str = "daily") -> None:
    """
    Save horoscopes to disk for a specific period.
    
    Args:
        horoscopes: Dictionary with structure {sign: text}
        period: Time period (daily, yesterday, tomorrow, weekly, monthly)
    """
    if period not in VALID_PERIODS:
        logger.error(f"Invalid period: {period}")
        return
    
    try:
        file_path = get_data_file_path()
        
        # Load existing data if it exists
        existing_data = {}
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        
        # Update with new data
        if "horoscopes" not in existing_data:
            existing_data["horoscopes"] = {}
        
        existing_data["horoscopes"][period] = horoscopes
        existing_data["date"] = date.today().isoformat()
        existing_data["timestamp"] = datetime.now().isoformat()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {period} horoscopes to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save {period} horoscopes: {e}")


def load_horoscopes(period: str = "daily") -> Optional[Dict[str, str]]:
    """
    Load horoscopes from disk for a specific period.
    
    Args:
        period: Time period (daily, yesterday, tomorrow, weekly, monthly)
    
    Returns:
        Dictionary with horoscopes or None if not found
    """
    if period not in VALID_PERIODS:
        logger.error(f"Invalid period: {period}")
        return None
    
    try:
        file_path = get_data_file_path()
        if not file_path.exists():
            logger.info(f"No horoscope data found for {period}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if the data is from today
        saved_date = datetime.fromisoformat(data["date"]).date()
        if saved_date != date.today():
            logger.info("Saved data is not from today, will fetch fresh data")
            return None
        
        horoscopes = data.get("horoscopes", {})
        period_data = horoscopes.get(period, {})
        
        if period_data:
            logger.info(f"Loaded {period} horoscopes from {file_path}")
            return period_data
        else:
            logger.info(f"No {period} horoscopes found in saved data")
            return None
            
    except Exception as e:
        logger.error(f"Failed to load {period} horoscopes: {e}")
        return None


def save_daily_horoscopes(horoscopes: Dict[str, Dict[str, str]]) -> None:
    """
    Legacy function for backward compatibility.
    Save daily horoscopes to disk.
    
    Args:
        horoscopes: Dictionary with structure {sign: {period: text}}
    """
    # Extract daily horoscopes and save them
    daily_horoscopes = {}
    for sign, periods in horoscopes.items():
        if "daily" in periods:
            daily_horoscopes[sign] = periods["daily"]
    
    save_horoscopes(daily_horoscopes, "daily")


def load_daily_horoscopes() -> Optional[Dict[str, Dict[str, str]]]:
    """
    Legacy function for backward compatibility.
    Load today's horoscopes from disk.
    
    Returns:
        Dictionary with horoscopes or None if not found
    """
    daily_data = load_horoscopes("daily")
    if daily_data:
        # Convert to legacy format
        return {sign: {"daily": text} for sign, text in daily_data.items()}
    return None


def is_data_fresh(period: str = "daily") -> bool:
    """
    Check if we have fresh data for today and specific period.
    
    Args:
        period: Time period to check
    
    Returns:
        True if fresh data exists, False otherwise
    """
    if period not in VALID_PERIODS:
        return False
    
    file_path = get_data_file_path()
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        saved_date = datetime.fromisoformat(data["date"]).date()
        if saved_date != date.today():
            return False
        
        # Check if the specific period exists
        horoscopes = data.get("horoscopes", {})
        return period in horoscopes and bool(horoscopes[period])
    except Exception:
        return False


def cleanup_old_data(days_to_keep: int = 7) -> None:
    """
    Clean up old horoscope data files.
    
    Args:
        days_to_keep: Number of days of data to keep
    """
    try:
        cutoff_date = date.today() - datetime.timedelta(days=days_to_keep)
        
        for file_path in DATA_DIR.glob("horoscopes_*.json"):
            try:
                # Extract date from filename
                date_str = file_path.stem.split("_")[1]
                file_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                
                if file_date < cutoff_date:
                    file_path.unlink()
                    logger.info(f"Deleted old data file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to process file {file_path}: {e}")
    except Exception as e:
        logger.error(f"Failed to cleanup old data: {e}") 