from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class ActivityLog(BaseModel):
    action: str
    timestamp: datetime

class User(BaseModel):
    username: str
    email: EmailStr
    role: str

class UserCreate(User):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(User):
    userid: str
    activitylog: Optional[List[ActivityLog]] = []