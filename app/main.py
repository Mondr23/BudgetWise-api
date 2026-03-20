from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import Base, engine

# import ALL models so SQLAlchemy knows them
from app.models import review, city, travel_cost, user 

# Routers
from app.routers.countries_router import router as countries_router
from app.routers.weather_router import router as weather_router
from app.routers.tourism_router import router as tourism_router
from app.routers.cities_router import router as cities_router
from app.routers.costs_router import router as costs_router
from app.routers.reviews_router import router as reviews_router
from app.routers.auth_router import router as auth_router
from app.routers.summery import router as destination_router
from app.routers.recommendations import router as recommendations_router
from app.routers.compare_router import router as compare_router


app = FastAPI(
    title="BudgetWise Travel API",
    version="2.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# CREATE TABLES
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# Routers
app.include_router(auth_router)
app.include_router(countries_router)
app.include_router(cities_router)
app.include_router(weather_router)
app.include_router(costs_router)
app.include_router(tourism_router)
app.include_router(reviews_router)
app.include_router(destination_router)
app.include_router(compare_router)
app.include_router(recommendations_router)



@app.get("/")
def root():
    return {"message": "API running"}