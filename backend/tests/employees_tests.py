from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
#this function will create an employee before the test and delete it after the test
#because we need an existing employee to test the update, delete and get by department functionality
def create_employee(client, employee_data):
    # Setup
    response = client.post("/employees/employee", json=employee_data)
    assert response.status_code == 201

    yield employee_data  # pass data to test

    # Cleanup
    client.delete(f"/employees/{employee_data['employeeId']}")

#GET all employees test case
def test_get_employees(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)



#POST request to add a new employee test case
def test_add_employee(client, employee_data):
    response = client.post("/employees/employee", json=employee_data)
    assert response.status_code == 201
    assert response.json().get("message") == "Employee added successfully"

    # Verify
    get_response = client.get("/employees")
    assert any(emp["employeeId"] == employee_data["employeeId"] for emp in get_response.json())

    # Cleanup
    client.delete(f"/employees/{employee_data['employeeId']}")



#   UPDATE employee
def test_update_employee(client, create_employee):
    updated_data = create_employee.copy()
    updated_data["position"] = "Senior Tester"

    response = client.put(f"/employees/{create_employee['employeeId']}", json=updated_data)

    assert response.status_code == 200
    assert response.json().get("message") == "Employee updated successfully"

# DELETE employee
def test_delete_employee(client, employee_data):
    # Create first
    client.post("/employees/employee", json=employee_data)

    response = client.delete(f"/employees/{employee_data['employeeId']}")

    assert response.status_code == 200
    assert response.json().get("message") == "Employee deleted successfully"

    # Verify deletion
    get_response = client.get(f"/employees/{employee_data['employeeId']}")
    assert get_response.status_code == 404

# GET by department
def test_get_employees_by_department(client, create_employee):
    dept = create_employee["department"]

    response = client.get(f"/employees/department/{dept}")

    assert response.status_code == 200
    assert any(emp["employeeId"] == create_employee["employeeId"] for emp in response.json())

#GET by ID
def test_get_employee_by_id(client, create_employee):
    emp_id = create_employee["employeeId"]

    response = client.get(f"/employees/{emp_id}")

    assert response.status_code == 200
    assert response.json().get("employeeId") == emp_id




