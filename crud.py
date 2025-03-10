from sqlalchemy.orm import Session
from auth import hash_password
from models import User, Pet
from schemas import PetCreate
from fastapi import HTTPException


# 🔹 Get User by Username
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# 🔹 Create User
def create_user(db: Session, username: str, password: str):
    hashed_pw = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 🔹 Create Pet
def create_pet(db: Session, owner_id: int, name: str, pet_type: str):
    new_pet = Pet(name=name, owner_id=owner_id, pet_type=pet_type)
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet

# 🔹 Get All Pets
def get_pets(db: Session):
    return db.query(Pet).all()

def adopt_pet(db: Session, user_id: int, pet_data: PetCreate):
    """Allows a user to adopt a pet but limits them to 2 pets max."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user already owns 2 pets
    if len(user.pets) >= 2:
        raise HTTPException(status_code=400, detail="You can only adopt up to 2 pets")

    # ✅ Assign `owner_id` automatically
    pet = Pet(name=pet_data.name, pet_type=pet_data.pet_type, owner_id=user_id)
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet