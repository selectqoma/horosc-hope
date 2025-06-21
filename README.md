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
