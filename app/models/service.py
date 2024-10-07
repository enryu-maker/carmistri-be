from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
import datetime


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    service_type = Column(String, nullable=False)
    pickup_location = Column(String, nullable=True)
    pickup_time = Column(DateTime, nullable=True)
    confirmed_service = Column(Boolean, default=False)
    manager_support = Column(String, nullable=True)
    service_status = Column(String, nullable=False)  # Could be Enum
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="services")
    garage_id = Column(Integer, ForeignKey('garages.id'))
    garage = relationship("Garage", back_populates="services")
