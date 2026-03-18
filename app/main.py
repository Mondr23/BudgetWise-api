from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.limiter import limiter
from app.routers import auth_router

# Routers
from app.routers import (
    countries_router,
    airports_router,
    weather_router,
    tourism_router,
    analytics_router,
    cities_router
)
from app.routers.health_router import router as health_router

# Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(
    title="Global Travel Intelligence API",
    version="1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Routers
app.include_router(countries_router.router)
app.include_router(airports_router.router)
app.include_router(weather_router.router)
app.include_router(tourism_router.router)
app.include_router(analytics_router.router)
app.include_router(cities_router.router)
app.include_router(health_router)
app.include_router(auth_router.router)

# Global error handler
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.get("/")
def root():
    return {"message": "API running"}