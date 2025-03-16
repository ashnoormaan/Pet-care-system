from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    pets = relationship("Pet", back_populates="owner")
    reviews = relationship("Review", back_populates="owner")

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    pet_type = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="pets")
    health_record = relationship("HealthRecord", back_populates="pet", uselist=False, cascade="all, delete-orphan")

class Caregiver(Base):
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    pet_types = Column(String, nullable=False)  # Comma-separated pet types
    is_active = Column(Boolean, default=True)

    # ✅ Fix conflicting relationships with overlaps
    bookings = relationship("Booking", back_populates="caregiver", overlaps="caregiver")
    reviews = relationship("Review", back_populates="caregiver") 

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

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    caregiver_id = Column(Integer, ForeignKey("caregivers.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="reviews")
    caregiver = relationship("Caregiver", back_populates="reviews")

class HealthRecord(Base):
    __tablename__ = "health_records"
    __table_args__ = {"extend_existing": True} 

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), unique=True)

    age_years = Column(Integer, nullable=True)
    age_months = Column(Integer, nullable=True)
    health_conditions = Column(String, nullable=True)
    allergies = Column(String, nullable=True)
    last_vaccination_date = Column(Date, nullable=True)
    vaccine_type = Column(String, nullable=True)
    medications = Column(String, nullable=True)
    vet_name = Column(String, nullable=True)
    vet_contact = Column(String, nullable=True)
    last_checkup_date = Column(Date, nullable=True)

    pet = relationship("Pet", back_populates="health_record")
