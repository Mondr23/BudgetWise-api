from pydantic import BaseModel

class CountrySchema(BaseModel):
    country_code: str
    country_name: str

    class Config:
        orm_mode = True