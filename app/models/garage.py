from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
import datetime


class Garage(Base):
    __tablename__ = "garages"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    services = relationship("Service", back_populates="garage")
