from pydantic import BaseModel

class AirportSchema(BaseModel):
    airport_id: int
    name: str
    iata: str
    icao: str

    class Config:
        orm_mode = True