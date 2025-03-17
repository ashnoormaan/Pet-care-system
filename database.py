from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./petcare.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def initialize_database():
    """Drops and recreates all tables in the database to match the updated schema."""
    import os
    if os.path.exists("petcare.db"):
        os.remove("petcare.db")  # Delete old database
    Base.metadata.create_all(bind=engine)
    
# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()