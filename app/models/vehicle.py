from sqlalchemy import String, Integer, Boolean, Column, ForeignKey, JSON
from app.database import Base
from sqlalchemy.orm import relationship


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    icon = Column(String, nullable=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    number = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  # Link to the User model
    user = relationship("User", back_populates="vehicles")
