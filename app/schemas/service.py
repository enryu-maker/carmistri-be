from pydantic import BaseModel


class ServiceSchema(BaseModel):
    service_type: str
    pickup_location: Optional[str]
    pickup_time: Optional[datetime]
    confirmed_service: bool
    manager_support: Optional[str]
    service_status: str

    class Config:
        orm_mode = True
