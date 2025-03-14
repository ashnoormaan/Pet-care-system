from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from schemas import UserCreate, UserResponse, PetCreate, PetResponse
from crud import create_user, create_pet, get_user, get_pets
from auth import create_access_token, verify_password, verify_access_token
from crud import adopt_pet
from models import User  # ✅ Ensure User model is imported


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
@router.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user.username)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ Verify the password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ Store the user ID (not username) in the token
    token = create_access_token({"sub": str(db_user.id)})

    return {"access_token": token, "token_type": "bearer"}


# 🔹 Get Current User (Protected)
@router.get("/me/", response_model=UserResponse)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    # ✅ Extract `user_id` from JWT token
    payload = verify_access_token(token)
    user_id = payload.get("sub")  # Extract user ID from token

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    # ✅ Convert `user_id` to an integer
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID in token")

    # ✅ Fetch user from the database
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user  # ✅ Return `UserResponse`


# 🔹 Add Pet
@router.post("/pets/", response_model=PetResponse)
def add_pet(
    pet: PetCreate,
    token: str = Depends(oauth2_scheme),  # ✅ Extract token from request
    db: Session = Depends(get_db),
):
    # ✅ Verify JWT token and extract user_id
    payload = verify_access_token(token)
    user_id = payload.get("sub")  # Extract user ID from the token

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    # ✅ Convert `user_id` to an integer to prevent errors
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID in token")

    return create_pet(db, user_id, pet.name, pet.pet_type)  # ✅ Use extracted user_id



# 🔹 List Pets
@router.get("/pets/", response_model=list[PetResponse])
def list_pets(db: Session = Depends(get_db)):
    return get_pets(db)

@router.post("/adopt/", response_model=PetResponse)
def adopt_pet_route(
    pet: PetCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # ✅ Extract `user_id` from the JWT token
    payload = verify_access_token(token)
    user_id = payload.get("sub")  # Extract user ID from the token
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    return adopt_pet(db, user_id, pet)