# 🐶 Pet Care Service API

This is a **FastAPI-based** backend for a **Pet Sitting** service.  
Users can **register, log in** and view their pets.

## 🚀 Features
- **User Registration & Authentication** (JWT-based)
- **List Pets** (Retrieve all pets adopted by a user)
- **Secure Authentication** (Using JWT for user sessions)
- **Database Integration** (SQLAlchemy with SQLite/PostgreSQL)
- **Testing with Pytest**
- **API Documentation** (OpenAPI & Swagger)
- **Adopt pets** (A user can not adopt more than 2 pets)
- **Register as a caregiver** (You can specify the type of pets that you are willing to take care of)
- **Book caregivers** (As a pet owner you can book a caregiver for your pet)
---

## 🛠️ Tech Stack
- **FastAPI** - API framework
- **SQLAlchemy** - ORM for database
- **Pydantic** - Data validation
- **PyJWT** - Authentication
- **Uvicorn** - ASGI server
- **Poetry** - Dependency management
- **pytest** - Unit testing

---

## 🔧 Installation & Setup

1️⃣ **Clone the Repository**
git clone https://github.com/yourusername/pet-care-api.git
cd pet-care-api

2️⃣ Install Dependencies
python -m pip install --upgrade pip
python -m pipx install poetry
poetry install

3️⃣ Configure Virtual Environment
poetry shell

4️⃣ Run the API
python main.py

API will be available at: http://127.0.0.1:8000/docs
