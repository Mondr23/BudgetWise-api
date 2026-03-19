from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base

class Weather(Base):
    __tablename__ = "weather"

    weather_id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.city_id"))
    condition = Column(String)
 