from pydantic import BaseModel
from typing import Optional, Dict


class VehicleBase(BaseModel):
    icon: Optional[str]
    make: str
    model: str
    number: str


class VehicleCreate(VehicleBase):
    pass


class VehicleResponse(VehicleBase):
    id: int
    user_id: Optional[int] = None  # Optional if not included in all responses

    class Config:
        orm_mode = True
