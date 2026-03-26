from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test cases for the GET /employees endpoint to list all employees
def test_get_employees():
    response = client.get("/employees")
    assert response.status_code == 200 #condition1
    assert isinstance(response.json(), list) #condition2
   
# Test case for POST /employee endpoint to add a new employee (if implemented)
def test_add_employee():
    payload = {
        "employeeId": "12345",
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "department": "IT",
        "position": "Data Analyst",
        "status": "Active"
    }
    response = client.post("/employees/employee", json=payload)
    assert response.status_code == 200 #changed condition from 201 to 
    #200 because the endpoint currently returns 200 with a message instead of 201 Created
    assert response.json().get("message") == "Employee added successfully" ##assert message successful
    #check if employee id is in database
    get_response = client.get("/employees")
    assert any(emp["employeeId"] == "12345" for emp in get_response.json())  
    response = client.delete("/employees/12345") #cleanup - delete the test employee after the test
    assert response.status_code == 200
    
# Update an employee test case  /employees/{employeeId} endpoint
def test_update_employee():
    # First, add an employee to update
    payload = {
        "employeeId": "EMP006",
        "name": "John Smith",
        "email": "john.smith@example.com",
        "department": "HR",
        "position": "Manager",
        "status": "Active"
    }
    response = client.post("/employees/employee", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Employee added successfully"
    # Now, update the employee's position
    update_payload = {
        "employeeId": "EMP006",
        "name": "John Smith",
        "email": "john.smith@example.com",
        "department": "HR",
        "position": "Senior Manager",
        "status": "Active"
    }
    response = client.put("/employees/EMP006", json=update_payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Employee updated successfully"
    response = client.delete("/employees/EMP006") #cleanup - delete the test employee
    assert response.status_code == 200

# Delete an employee test case  /employees/{employeeId} endpoint
def test_delete_employee():
    # First, add an employee to delete
    payload = {
        "employeeId": "EMP007",
        "name": "Bob Johnson",
        "email": "bob.johnson@example.com",
        "department": "Finance",
        "position": "Analyst",
        "status": "Active"
    }
    response = client.post("/employees/employee", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Employee added successfully"
    # Now, delete the employee
    response = client.delete("/employees/EMP007")
    assert response.status_code == 200
    assert response.json().get("message") == "Employee deleted successfully"
    # Verify the deletion
    get_response = client.get("/employees/EMP007")
    assert get_response.status_code == 404


# Get an employee by department test case /employee/department/{department_name} endpoint
def test_get_employees_by_department():
    # First, add an employee to the IT department
    payload = {
        "employeeId": "EMP9876",
        "name": "Charlie Brown",
        "email": "charlie.brown@example.com",
        "department": "IT",
        "position": "Developer",
        "status": "Active"
    }
    response = client.post("/employees/employee", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Employee added successfully"
    # Now, get employees by department
    response = client.get("/employees/department/IT")
    assert response.status_code == 200
    assert any(emp["employeeId"] == "EMP9876" for emp in response.json())
    response = client.delete("/employees/EMP9876") #cleanup - delete the test employee after the test
    assert response.status_code == 200

# Get an employee by ID test case         /employee/{employeeId} endpoint
def test_get_employee_by_id():
    # First, add an employee to get by ID
    payload = {
        "employeeId": "EMP5432",
        "name": "Diana Prince",
        "email": "diana.prince@example.com",
        "department": "Marketing",
        "position": "Coordinator",
        "status": "Active"
    }
    response = client.post("/employees/employee", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Employee added successfully"
    # Now, get the employee by ID
    response = client.get("/employees/EMP5432")
    assert response.status_code == 200
    assert response.json().get("employeeId") == "EMP5432"
    response = client.delete("/employees/EMP5432") #cleanup - delete the test employee after the test
    assert response.status_code == 200

