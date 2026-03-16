from fastapi import FastAPI
from app.routers import (
    countries_router,
    airports_router,
    weather_router,
    tourism_router,
    analytics_router
)
from app.routers import cities_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Global Travel Intelligence API",
    description="API for analyzing global travel destinations",
    version="1.0"
)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(countries_router.router)
app.include_router(airports_router.router)
app.include_router(weather_router.router)
app.include_router(tourism_router.router)
app.include_router(analytics_router.router)
app.include_router(cities_router.router)

@app.get("/")
def root():
    return {"message": "Global Travel Intelligence API running"}