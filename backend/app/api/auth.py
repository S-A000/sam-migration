from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt # PyJWT library


router = APIRouter()

SECRET_KEY = "super-secret-saas-key" # Isko hamesha hide rakhna hai
ALGORITHM = "HS256"

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. User ko database mein check karein (Fake check for now)
    if form_data.username == "alex@enterprise.com" and form_data.password == "admin123":
        
        # 2. Token tayaar karein
        expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode = {"sub": form_data.username, "exp": expire, "role": "System Architect"}
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "access_token": encoded_jwt, 
            "token_type": "bearer",
            "user": {"name": "Alex Chen", "role": "System Architect"}
        }
    
    raise HTTPException(status_code=400, detail="Invalid Email or Password")