from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from app.database import Base 


class City(Base):

    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String)
    country_code = Column(String, ForeignKey("countries.country_code"))

    __table_args__ = (
        UniqueConstraint("city_name", "country_code", name="unique_city_country"),
    )