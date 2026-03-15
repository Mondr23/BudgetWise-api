from sqlalchemy import Column, String
from app.database import Base

class Country(Base):
    __tablename__ = "countries"

    country_code = Column(String, primary_key=True)
    country_name = Column(String)