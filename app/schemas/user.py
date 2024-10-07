from pydantic import BaseModel, Field
from typing import List, Optional
from .vehicle import VehicleResponse


class UserResponse(BaseModel):
    id: int
    icon: Optional[str] = None
    full_name: str
    email: str
    mobile_number: str
    is_verified: bool
    vehicles: List[VehicleResponse] = []

    class Config:
        orm_mode = True  # Allows the Pydantic model to work with SQLAlchemy objects


class UserCreate(BaseModel):
    icon: str
    full_name: str
    email: str
    mobile_number: str


class OTPVerify(BaseModel):
    mobile_number: str
    otp: str
