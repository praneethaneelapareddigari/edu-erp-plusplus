import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.hash import bcrypt

auth_router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Very simple in-memory user (for demo). In real setup, use Frappe users or DB.
USERS = {
    "admin@example.com": bcrypt.hash("admin123")
}

def create_token(sub: str):
    payload = {
        "sub": sub,
        "exp": datetime.utcnow() + timedelta(hours=8),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return payload["sub"]

@auth_router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if username not in USERS or not bcrypt.verify(password, USERS[username]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": create_token(username), "token_type": "bearer"}
