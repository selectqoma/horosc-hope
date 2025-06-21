#!/usr/bin/env python3
"""
Simple script to run the HoroscHope application.
"""
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000, reload=True) 