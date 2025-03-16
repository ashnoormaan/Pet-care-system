from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from auth import hash_password
from models import User, Pet, Caregiver, Booking, Review
from schemas import PetCreate, CaregiverCreate, BookingCreate, ReviewCreate
from fastapi import HTTPException
from datetime import datetime

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

# 🔹 Create Caregiver
def create_caregiver(db: Session, caregiver: CaregiverCreate):
    existing_caregiver = db.query(Caregiver).filter(Caregiver.username == caregiver.username).first()

    if existing_caregiver:
        raise HTTPException(status_code=400, detail="A caregiver with this username already exists")

    hashed_password = hash_password(caregiver.password)  # Ensure password is hashed

    db_caregiver = Caregiver(
        username=caregiver.username,
        hashed_password=hashed_password,  # ✅ Store only hashed password
        pet_types=caregiver.pet_types,
        is_active=True
    )

    db.add(db_caregiver)
    db.commit()
    db.refresh(db_caregiver)

    return db_caregiver  # ✅ No password field in response


# 🔹 Get Available Caregivers
def get_caregivers(db: Session):
    return db.query(Caregiver).all()

# 🔹Create booking
def create_booking(db: Session, booking_data: BookingCreate):
    caregiver = db.query(Caregiver).filter(Caregiver.id == booking_data.caregiver_id, Caregiver.is_active == True).first()
    if not caregiver:
        raise HTTPException(status_code=404, detail="Caregiver not found or no longer available")

    pet = db.query(Pet).filter(Pet.id == booking_data.pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    allowed_pet_types = caregiver.pet_types.split(", ")
    if pet.pet_type not in allowed_pet_types:
        raise HTTPException(status_code=400, detail=f"Caregiver does not take care of {pet.pet_type}")

    new_booking = Booking(
        pet_id=booking_data.pet_id,
        caregiver_id=booking_data.caregiver_id,
        date=booking_data.date,
        time_from=booking_data.time_from,
        time_to=booking_data.time_to
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

# 🔹 Get All Bookings
def get_bookings(db: Session):
    return db.query(Booking).all()

current_datetime = datetime.now()
current_date = current_datetime.date()  # Extracts YYYY-MM-DD
current_time = current_datetime.time()  # Extracts HH:MM:SS

# 🔹 Update expired caregivers and bookings
from datetime import datetime

from datetime import datetime

def update_expired_availability(db):
    caregivers = db.query(Caregiver).all()
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    for caregiver in caregivers:
        for booking in caregiver.bookings:  # Assuming Caregiver has `bookings` relationship
            try:
                # ✅ Handle cases where booking.date includes time
                if " " in booking.date:  
                    booking_date = datetime.strptime(booking.date.split(" ")[0], "%Y-%m-%d").date()
                else:
                    booking_date = datetime.strptime(booking.date, "%Y-%m-%d").date()

                # ✅ Handle 12-hour format (AM/PM)
                booking_time_to = datetime.strptime(booking.time_to, "%I:%M %p").time()

            except ValueError:
                print(f"Invalid date/time format in booking: {booking.date} {booking.time_to}")
                continue  # Skip this booking if format is wrong

            # ✅ Compare correctly
            if booking_date < current_date or (booking_date == current_date and booking_time_to <= current_time):
                booking.status = "expired"

    db.commit()


def create_review(db: Session, owner_id: int, review_data: ReviewCreate):
    if review_data.rating < 1 or review_data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    new_review = Review(
        owner_id=owner_id,
        caregiver_id=review_data.caregiver_id,
        rating=review_data.rating,
        comment=review_data.comment,
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def get_reviews_by_caregiver(db: Session, caregiver_id: int):
    return db.query(Review).filter(Review.caregiver_id == caregiver_id).all()
