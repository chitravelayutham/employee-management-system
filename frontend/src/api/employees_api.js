import API from "./api"

// Fetch all employees
export const getEmployees = () => API.get("/employees")

// Create a new employee
export const createEmployee = (employee) => API.post("/employees/employee", employee)

// Update an existing employee
export const updateEmployee = (id, employee) => API.put(`/employees/${id}`, employee)

// Delete an employee
export const deleteEmployee = (id) => API.delete(`/employees/${id}`)
