from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base

class Weather(Base):
    __tablename__ = "weather"

    weather_id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.city_id"))
    temperature = Column(Float)
    humidity = Column(Float)
    wind_kph = Column(Float)
    precipitation = Column(Float)
    visibility = Column(Float)
    air_quality_pm25 = Column(Float)
    condition = Column(String)
    last_updated = Column(String)