1. Bootstrapped APP
2. Connected to Mongo DB
3. Test Case to get all employees
4. Schema creation
5. Model implementation
6. Controller implementation
7. Routes / APIs


--empid"="EMP101" --name"="Test User Dynamic" --email="test.user@example.com" --department="IT" --position=="Tester" --status ="Active"

=====================================

=======================================


Context: I have an employee management web application whose backend runs on Python, FastAPI and MongoDb with MVC architecture. Using the below code:
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List

# ----- App & Security Setup -----
app = FastAPI()

SECRET_KEY = "mysecretkey123"  # JWT secret key (keep it secret in real apps)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto") # Using Argon2 for password hashing
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # Endpoint for token generation



# ----- Hardcoded Users -----
# Passwords are hashed for demonstration
users_db = {
    "admin": {"username": "admin", "password": pwd_context.hash("admin123"), "role": "admin"},
    "user": {"username": "user", "password": pwd_context.hash("user123"), "role": "user"},
}


# ----- Utility Functions -----
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        role = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        user = {"username": username, "role": role}
    except JWTError:
        raise credentials_exception
    return user

def admin_required(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return user

# ----- Routes -----
# Login → returns JWT token
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    print("Authenticated user:", user)  # Debugging statement
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token(
        data={"username": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


Task: Create a collection in MongoDB for users with userid, username, email, password, role and activitylog. 
Create separate files for user schema as user_schema.py(has pydantic model), 
user_routes.py for routes(register_new_user and login and calls functions in user_controller.py),
user_model.py for models (functions that queries db) 
and user_controller.py with functions to register new users and login existing users.
Create a function that captures and updates all the user activities.
Also, create an utils folder and utils.py file in it to capture all the authentication, password and JWT code. 
Add the SECRET_KEY,ALGORITHM ,ACCESS_TOKEN_EXPIRE_MINUTES in env file.

