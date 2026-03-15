from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Airport(Base):
    __tablename__ = "airports"

    airport_id = Column(Integer, primary_key=True)
    name = Column(String)
    iata = Column(String)
    icao = Column(String)
    city_id = Column(Integer, ForeignKey("cities.city_id"))
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String)