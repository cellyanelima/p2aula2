from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re

app = FastAPI(title="Name and Email Standardization System")

# Database configuration (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy model for the database
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic model for data validation
class UserBase(BaseModel):
    name: str
    email: EmailStr

# Function to standardize name
def standardize_name(name: str) -> str:
    # Remove extra spaces and convert to lowercase
    name = " ".join(name.split()).lower()

    # Capitalize each word
    name = name.title()

    # Handle prepositions like 'da', 'de', 'do', 'das', 'dos' is important because full names of people may contain them.
    prepositions = ['Da', 'De', 'Do', 'Das', 'Dos']
    words = name.split()
    final_name = []
    
    for word in words:
        if word in prepositions:
            final_name.append(word.lower())
        else:
            final_name.append(word)
    
    return " ".join(final_name)
