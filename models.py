from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    pets = relationship("Pet", back_populates="owner")

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    pet_type = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="pets")

class Caregiver(Base):
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    pet_types = Column(String, nullable=False)  # Comma-separated pet types
    is_active = Column(Boolean, default=True)

    # ✅ Fix conflicting relationships with overlaps
    bookings = relationship("Booking", back_populates="caregiver", overlaps="caregiver")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    caregiver_id = Column(Integer, ForeignKey("caregivers.id"), nullable=False)
    date = Column(String, nullable=False)
    time_from = Column(String, nullable=False)
    time_to = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    caregiver = relationship("Caregiver", back_populates="bookings", overlaps="bookings")

