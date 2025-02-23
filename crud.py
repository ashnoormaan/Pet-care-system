from sqlalchemy.orm import Session
from database import User, Pet
from auth import hash_password

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
def create_pet(db: Session, name: str, owner_id: int, pet_type: str):
    new_pet = Pet(name=name, owner_id=owner_id, pet_type=pet_type)
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet

# 🔹 Get All Pets
def get_pets(db: Session):
    return db.query(Pet).all()
