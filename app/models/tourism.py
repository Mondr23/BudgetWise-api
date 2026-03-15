from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Tourism(Base):
    __tablename__ = "tourism_statistics"

    tourism_id = Column(Integer, primary_key=True)
    country_code = Column(String, ForeignKey("countries.country_code"))
    year = Column(Integer)
    tourist_arrivals = Column(Integer)