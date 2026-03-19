from pydantic import BaseModel, constr, field_validator


class CountrySchema(BaseModel):
    """
    Country schema with validation + ORM support
    """

    country_code: constr(min_length=2, max_length=3)
    country_name: constr(min_length=2, max_length=100)

    # --- VALIDATION ---
    @field_validator("country_code")
    def validate_code(cls, v):
        return v.strip().upper()

    @field_validator("country_name")
    def validate_name(cls, v):
        return v.strip().title()

    class Config:
        from_attributes = True