from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.model.user_model import get_user_by_username

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Password hashing
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# JWT Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    print("Decoding token in decode_token function:", token)  # Debugging line
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])



# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if not token:
        print("No token provided.")
        raise credentials_exception

    try:
        payload = decode_token(token)
    except JWTError as e:
        print(f"JWTError during token decoding: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"Unexpected error during token decoding: {e}")
        raise credentials_exception

    if not isinstance(payload, dict):
        print(f"Decoded payload is not a dict: {payload}")
        raise credentials_exception

    username = payload.get("username")
    if not username:
        print(f"Username not found in token payload: {payload}")
        raise credentials_exception

    user = get_user_by_username(username)
    if not user:
        print(f"User '{username}' not found in database.")
        raise credentials_exception

    return user

#RBAC - generic role checker
def role_required(required_roles: list):
    def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return user
    return role_checker


#RBAC - admin only
def admin_required(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user
