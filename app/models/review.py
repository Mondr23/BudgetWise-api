from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.city_id"))

    user_name = Column(String)

    
    money_spent = Column(Float)
    trip_days = Column(Integer)
    value_rating = Column(Float)

    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)