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

# Function to standardize email (based on the name)
def standardize_email(name: str) -> str:
    # Remove diacritics/accents
    from unicodedata import normalize
    name = normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    
    # Lowercase and replace spaces with dots
    email = name.lower().replace(' ', '.')

    # Remove special characters (keep only letters, numbers and dots)
    email = re.sub(r'[^a-z0-9.]', '', email)
    
    # Remove duplicated dots
    email = re.sub(r'\.+', '.', email)
    
    # Trim dots at the start or end
    email = email.strip('.')
    
    # Use an English-style domain
    return f"{email}@company.com.br"

@app.get("/")
async def welcome():
    return {"message": "Welcome to the Name and Email Standardization System"}

@app.post("/users/")
async def create_user(user: UserBase):
    standardized_name = standardize_name(user.name)
    standardized_email = standardize_email(standardized_name)
    
    db = SessionLocal()
    try:
        new_user = User(name=standardized_name, email=standardized_email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "details": {
                "original_name": user.name,
                "standardized_name": standardized_name,
                "generated_email": standardized_email
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.get("/users/")
async def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        # Return as plain dicts to ensure JSON serialization
        return [{"id": u.id, "name": u.name, "email": u.email} for u in users]
    finally:
        db.close()
