from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Database URL (Asal mein yeh .env se aayegi)
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/migration_saas_db"

# Engine tayaar karein
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session factory banayein
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Database session ko request ke liye open/close karne ka generator"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()