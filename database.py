# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# import sqlite3

# Base = declarative_base()  # ✅ Only define Base here

# DATABASE_URL = "sqlite:///./pets.db"  # Change for PostgreSQL/MySQL if needed
# DB_FILE = "pets.db"

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def initialize_database():
#     """Creates all tables in the database."""
#     Base.metadata.create_all(bind=engine)

# # ✅ Connect to the SQLite database
# conn = sqlite3.connect(DB_FILE)
# cursor = conn.cursor()

# # ✅ Check if `available_dates` column exists
# cursor.execute("PRAGMA table_info(caregivers);")
# columns = [column[1] for column in cursor.fetchall()]

# conn.commit()
# conn.close()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "sqlite:///./petcare.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def initialize_database():
#     """Creates all tables in the database if they don't exist."""
#     Base.metadata.create_all(bind=engine)

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

