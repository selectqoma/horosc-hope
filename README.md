# HoroscHope

Backend project providing roasted horoscope data.

## Setup

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Export your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```
3. Run the API:
   ```bash
   uvicorn backend.api.main:app --reload
   ```

## Frontend

A minimal React-based frontend is available in the `frontend/` directory. It uses CDN versions of React so no build step is required. Run a simple HTTP server to view it locally:

```bash
python -m http.server 3000 -d frontend
```

Open `http://localhost:3000` in your browser while the backend API is running on `http://localhost:8000`.
