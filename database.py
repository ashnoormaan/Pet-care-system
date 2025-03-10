from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()  # ✅ Only define Base here

DATABASE_URL = "sqlite:///./pets.db"  # Change for PostgreSQL/MySQL if needed

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
