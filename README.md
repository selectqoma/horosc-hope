# HoroscHope

Backend project providing roasted horoscope data.

## Setup

1. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create virtual environment and install dependencies:
   ```bash
   uv venv
   uv pip install -e .
   ```

3. Set up environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=your-actual-api-key-here
   ```

4. Run the application:

   **Option 1: Run both backend and frontend together (recommended for development):**
   ```bash
   uv run python run_dev.py
   ```

   **Option 2: Run services separately:**
   ```bash
   # Backend API
   uv run python run.py
   
   # Frontend (in another terminal)
   uv run python -m http.server 3000 -d frontend
   ```

   **Option 3: Using uv run with uvicorn directly:**
   ```bash
   uv run uvicorn backend.api.main:app --reload
   ```

## Development

To install development dependencies:
```bash
uv pip install --group dev
```

## Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Frontend

A minimal React-based frontend is available in the `frontend/` directory. It uses CDN versions of React so no build step is required. The frontend will automatically connect to the backend API running on `http://localhost:8000`.
