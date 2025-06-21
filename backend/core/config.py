"""
Configuration module for HoroscHope application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    @classmethod
    def validate(cls) -> None:
        """Validate that all required environment variables are set."""
        if not cls.OPENAI_API_KEY:
            raise EnvironmentError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file or export it in your shell."
            )
    
    @classmethod
    def get_openai_api_key(cls) -> str:
        """Get OpenAI API key with validation."""
        cls.validate()
        return cls.OPENAI_API_KEY 