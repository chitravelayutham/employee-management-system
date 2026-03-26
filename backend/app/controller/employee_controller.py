# Controller for employee-related operations / business logic

from fastapi import HTTPException
from app.model.employee_model import (
    get_all_employees,
    add_employee,
    update_one_employee,
    delete_employee,
    get_employees_by_department
)
from app.schemas.employee_schema import Employee, EmployeeCreate, EmployeeUpdate


# -------------------- COMMON HELPERS --------------------

def _get_all_employees_data():
    return get_all_employees()


def _format_employees(employee_list):
    return [Employee(**emp) for emp in employee_list]


def _find_employee_by_id(employee_id: str, employees: list):
    for emp in employees:
        if emp.get("employeeId") == employee_id:
            return emp
    return None


def _employee_exists(employee_id: str) -> bool:
    employees = _get_all_employees_data()
    return any(emp.get("employeeId") == employee_id for emp in employees)


# -------------------- GET ALL --------------------

def fetch_all_employees():
    employees = _get_all_employees_data()
    return _format_employees(employees)


# -------------------- CREATE --------------------

def _prepare_employee_data(employee: EmployeeCreate):
    return employee.model_dump()


def _insert_employee(employee_data: dict):
    return add_employee(employee_data)


def create_employee(employee: EmployeeCreate):
    if _employee_exists(employee.employeeId):
        return {"error": "Employee already exists"}

    employee_data = _prepare_employee_data(employee)
    result = _insert_employee(employee_data)

    if result.inserted_id:
        return {"message": "Employee added successfully"}

    raise HTTPException(status_code=500, detail="Failed to add employee")


# -------------------- UPDATE --------------------

def _prepare_update_data(employee_data: EmployeeUpdate):
    return employee_data.model_dump()


def _update_employee_in_db(employeeId: str, employee_data: dict):
    return update_one_employee(employeeId, employee_data)


def update_an_employee(employeeId: str, employee_data: EmployeeUpdate):
    if not _employee_exists(employeeId):
        return {"error": "Employee not found"}

    update_data = _prepare_update_data(employee_data)
    result = _update_employee_in_db(employeeId, update_data)

    if result.modified_count > 0:
        return {"message": "Employee updated successfully"}

    raise HTTPException(status_code=500, detail="Failed to update employee")


# -------------------- DELETE --------------------

def _delete_employee_from_db(employeeId: str):
    return delete_employee(employeeId)


def remove_employee(employeeId: str):
    result = _delete_employee_from_db(employeeId)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee deleted successfully"}


# -------------------- GET BY DEPARTMENT --------------------
def fetch_employees_by_department(department_name: str):
    employees = _get_all_employees_data()
    department_lower = department_name.strip().lower()
    filtered = [
        emp for emp in employees
        if department_lower in emp.get("department", "").strip().lower()
    ]
    if not filtered:
        raise HTTPException(status_code=404, detail="Department not found")
    return filtered

# -------------------- GET BY NAME --------------------

def _normalize_name(name: str):
    return name.strip().lower()


def _filter_employees_by_name(name: str, employees: list):
    name_lower = _normalize_name(name)
    return [
        emp for emp in employees
        if name_lower in emp.get("name", "").strip().lower()
    ]


def fetch_employees_by_name(name: str):
    employees = _get_all_employees_data()

    if not employees:
        raise HTTPException(status_code=404, detail="Employee not found")

    return _filter_employees_by_name(name, employees)


# -------------------- GET BY ID --------------------

def fetch_employee_by_id(employeeId: str):
    employees = _get_all_employees_data()
    emp = _find_employee_by_id(employeeId, employees)

    if emp:
        return Employee(**emp)

    raise HTTPException(status_code=404, detail="Employee not found")