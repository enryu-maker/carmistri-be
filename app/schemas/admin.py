from pydantic import BaseModel


class AdminResponse(BaseModel):
    id: int
    username: str
    password: str

    class Config:
        orm_mode = True  # Allows the Pydantic model to work with SQLAlchemy objects


class AdminCreate(BaseModel):
    username: str
    password: str
