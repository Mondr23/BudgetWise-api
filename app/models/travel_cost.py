from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base

class TravelCost(Base):
    __tablename__ = "travel_costs"

    cost_id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.city_id"))
    meal_price = Column(Float)
    coffee_price = Column(Float)
    beer_price = Column(Float)
    transport_ticket = Column(Float)
    taxi_km = Column(Float)
    rent_city_center = Column(Float)
    avg_salary = Column(Float)
    daily_accommodation = Column(Float)
    daily_cost_estimate = Column(Float)