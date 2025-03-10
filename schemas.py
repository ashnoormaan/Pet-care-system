
from pydantic import BaseModel

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
