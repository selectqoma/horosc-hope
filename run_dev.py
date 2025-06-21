#!/usr/bin/env python3
"""
Development script to run both backend and frontend servers.
"""
import subprocess
import sys
import time
import threading
import signal
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_backend():
    """Run the backend server."""
    print("🚀 Starting backend server on http://localhost:8000")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "backend.api.main:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

def run_frontend():
    """Run the frontend server."""
    print("🎨 Starting frontend server on http://localhost:3000")
    subprocess.run([
        sys.executable, "-m", "http.server", 
        "3000", 
        "-d", "frontend"
    ])

def main():
    print("🌟 Starting HoroscHope development servers...")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:3000")
    print("Press Ctrl+C to stop both servers")
    print("-" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend a moment to start
    time.sleep(2)
    
    # Start frontend in main thread
    run_frontend()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        sys.exit(0) 