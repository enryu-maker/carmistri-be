from sqlalchemy import String, Integer, Boolean, Column, ForeignKey, DateTime, Float
from app.database import Base
from sqlalchemy.orm import relationship
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    icon = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    mobile_number = Column(String, unique=True, index=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    vehicles = relationship("Vehicle", back_populates="user")
    services = relationship("Service", back_populates="user")
