from fastapi import FastAPI
from .routes.horoscope import router as horoscope_router

app = FastAPI(title="HoroscHope API")
app.include_router(horoscope_router)


@app.get("/")
def read_root():
    return {"message": "HoroscHope API"}
