from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from schemas import UserCreate, UserResponse, PetCreate, PetResponse
from crud import create_user, create_pet, get_user, get_pets
from auth import create_access_token, verify_password, verify_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 User Registration
@router.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user.username, user.password)

# 🔹 User Login
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# 🔹 Get Current User (Protected)
@router.get("/me/", response_model=UserResponse)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = get_user(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

# 🔹 Add Pet
@router.post("/pets/", response_model=PetResponse)
def add_pet(pet: PetCreate, db: Session = Depends(get_db)):
    return create_pet(db, pet.name, pet.owner_id, pet.pet_type)

# 🔹 List Pets
@router.get("/pets/", response_model=list[PetResponse])
def list_pets(db: Session = Depends(get_db)):
    return get_pets(db)
