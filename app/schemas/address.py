from pydantic import BaseModel, ConfigDict, Field, field_validator


class AddressBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, examples=["Home"])
    street: str = Field(..., min_length=1, max_length=255, examples=["123 Main St"])
    city: str = Field(..., min_length=1, max_length=100, examples=["Springfield"])
    state: str = Field(..., min_length=1, max_length=100, examples=["IL"])
    zip_code: str = Field(..., min_length=1, max_length=20, examples=["62701"])
    latitude: float = Field(..., ge=-90.0, le=90.0, examples=[39.7817])
    longitude: float = Field(..., ge=-180.0, le=180.0, examples=[-89.6501])

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: float) -> float:
        if not -90.0 <= value <= 90.0:
            raise ValueError("latitude must be between -90 and 90")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        if not -180.0 <= value <= 180.0:
            raise ValueError("longitude must be between -180 and 180")
        return value


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressResponse(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
