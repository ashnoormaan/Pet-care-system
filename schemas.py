from pydantic import BaseModel

# User Schema
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# Pet Schema
class PetCreate(BaseModel):
    name: str
    owner_id: int
    pet_type: str

class PetResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    pet_type: str

    class Config:
        orm_mode = True
