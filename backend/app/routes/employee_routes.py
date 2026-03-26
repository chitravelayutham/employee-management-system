#All API routes are defined here
from fastapi import APIRouter, Depends
from app.controller.employee_controller import fetch_all_employees, create_employee, update_an_employee, remove_employee, fetch_employees_by_department, fetch_employees_by_name, fetch_employee_by_id
from app.schemas.employee_schema import Employee, EmployeeCreate, EmployeeUpdate
from app.utils.utils import role_required

router = APIRouter()

#GET endpoint to list all employees depends on generic and add RBAC now, only admin and user can access this endpoint
@router.get("/", response_model=list[Employee], status_code=200, dependencies=[Depends(role_required(["admin", "user"]))])    
def get_employees():
    return fetch_all_employees()


#POST endpoint to add a new employee
@router.post("/employee", status_code=201, dependencies=[Depends(role_required(["admin"]))]) 
def add_employee(employee: EmployeeCreate):
    return  create_employee(employee)

#UPDATE endpoint to update an existing employee
@router.put("/{employeeId}", status_code=200)
def put_employee(employeeId: str, employee_data: EmployeeUpdate):
    return  update_an_employee(employeeId, employee_data) 


#DELETE endpoint to delete an employee
@router.delete("/{employeeId}", status_code=200)
def delete_employee(employeeId: str):
    return remove_employee(employeeId)

#GET endpoint to get employee by department
@router.get("/department/{department_name}", response_model=list[Employee], status_code=200)
def get_employees_by_department(department_name: str):
    return fetch_employees_by_department(department_name)
    
    
 #GET an employee by name
#Dont use /search as it will be a conflict with /employeeId route!!!
@router.get("/search", response_model=list[Employee], status_code=200) 
def get_employees_by_name(name: str):
    return fetch_employees_by_name(name)


#GET endpoint to get employee by employeeId
@router.get("/{employeeId}", response_model=Employee, status_code=200)
def get_employee_by_id(employeeId: str):
    return fetch_employee_by_id(employeeId)

