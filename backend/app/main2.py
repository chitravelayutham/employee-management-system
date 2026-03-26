from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

# Hardcoded users
users_db = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

# Sample data
employees = [
    {"id": 1, "name": "John Doe", "position": "Developer"},
    {"id": 2, "name": "Jane Smith", "position": "Manager"}
]

# Authentication function
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username not in users_db or users_db[username]["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": username, "role": users_db[username]["role"]}

# Admin-only function - RBAC
def admin_required(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user

# Endpoints
@app.get("/employees", dependencies=[Depends(get_current_user)])
def get_employees():
    return employees

@app.post("/employees", dependencies=[Depends(admin_required)])
def add_employee(employee: dict):
    employee["id"] = len(employees) + 1
    employees.append(employee)
    return employee

@app.get("/employees/{id}", dependencies=[Depends(get_current_user)])
def get_employee(id: int):
    for emp in employees:
        if emp["id"] == id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")

@app.put("/employees/{id}", dependencies=[Depends(admin_required)])
def update_employee(id: int, updated_employee: dict):
    for emp in employees:
        if emp["id"] == id:
            emp.update(updated_employee)
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employees/{id}", dependencies=[Depends(admin_required)])
def delete_employee(id: int):
    for emp in employees:
        if emp["id"] == id:
            employees.remove(emp)
            return {"detail": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Employee not found")