# Defines Employee schema for data validation and serialization
from pydantic import BaseModel, EmailStr
import datetime

class Employee(BaseModel):
    employeeId: str
    name: str
    email: EmailStr
    department: str
    position: str
    status: str

class EmployeeResponse(BaseModel):
    id : str
    createdAt: datetime.datetime

class EmployeeCreate(BaseModel):
    employeeId: str
    name: str
    email: EmailStr
    department: str
    position: str
    status: str
    createdAt: datetime.datetime = datetime.datetime.now()

class EmployeeUpdate(BaseModel):
    employeeId: str
    name: str | None = None
    email: EmailStr | None = None
    department: str | None = None
    position: str | None = None
    status: str | None = None
    updatedAt: datetime.datetime = datetime.datetime.now()