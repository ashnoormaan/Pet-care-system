from pydantic import BaseModel
from typing import Optional

# 🔹 User Schema
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # ✅ Pydantic v2 fix (Replaces orm_mode)

# 🔹 Pet Schema
class PetCreate(BaseModel):
    name: str
    pet_type: str  # ✅ Keep only name and pet_type

class PetResponse(PetCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# 🔹 Caregiver Schema


class CaregiverCreate(BaseModel):
    username: str
    password: str  # ✅ This is only for request data
    pet_types: str  # Comma-separated pet types

class CaregiverResponse(BaseModel):
    id: int
    username: str
    pet_types: str
    is_active: bool

    class Config:
        from_attributes = True

# 🔹 Booking Schema
class BookingCreate(BaseModel):
    pet_id: int
    caregiver_id: int
    date: str  # Example: "2025-02-23"
    time_from: str  # Example: "10:00 AM"
    time_to: str  # Example: "11:00 AM"

class BookingResponse(BookingCreate):
    id: int

    class Config:
        from_attributes = True