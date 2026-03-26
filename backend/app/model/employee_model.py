#Query the database for employee information
from app.config.database import employees_collection

#Get all employees from the database
def get_all_employees():
    return list(employees_collection.find({}, {"_id": 0}))

#POST request to add a new employee
def add_employee(employee_data: dict):
    return employees_collection.insert_one(employee_data)
  

#PUT request to update an existing employee
def update_one_employee(employeeId: str, employee_data: dict):
    return employees_collection.update_one({"employeeId": employeeId}, {"$set": employee_data})

#DELETE request to delete an employee
def delete_employee(employeeId: str):
    return employees_collection.delete_one({"employeeId": employeeId})

#GET request to get employees by department
def get_employees_by_department(department_name: str):  
    return list(employees_collection.find({"department": department_name}, {"_id": 0}))
