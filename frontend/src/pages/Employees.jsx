import React, { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { jwtDecode } from "jwt-decode";
import axios from "axios"

const Employees = () => {
// add state
  const [employees, setEmployees] = useState([])
  const [search, setSearch] = useState("")
  const [departmentFilter, setDepartmentFilter] = useState("")
  const [loading, setLoading] = useState(false)


  const navigate = useNavigate()

  const token = localStorage.getItem("access_token")
  const role = token ? jwtDecode(token).role : null
  const baseURL = "http://127.0.0.1:8000"

  useEffect(() => {
    let url = `${baseURL}/employees`;
    if (search) {
      url = `${baseURL}/employees/search?name=${encodeURIComponent(search)}`;
        } else if (departmentFilter) {
          url = `${baseURL}/employees/department/${encodeURIComponent(departmentFilter)}`;
    }

    setLoading(true);
    axios.get(url, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => {
        setEmployees(res.data);
        setLoading(false);
        console.log("API response:", res.data);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [token, search, departmentFilter])

  const handleDelete = (id) => {
    if (!token) {
      alert("Not authenticated. Please log in again.")
      return
    }
    if (!window.confirm("Are you sure you want to delete this employee?")) return
     axios.delete(`${baseURL}/employees/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
       .then(() => setEmployees(prev => prev.filter(emp => emp.employeeId !== id)))
      .catch(err => {
        console.error("Delete error details:", err.response?.data)
        alert("Failed to delete employee: " + (err.response?.data?.detail || err.message))
      })
  }

  return (
    <div className="employees-container">
      <div className="employees-header">
        <h1>Employee Management</h1>
        {/* Add Employee button only for admin */}
        {role === "admin" && (
          <button className="add-employee-btn" onClick={() => navigate("/employees/create")}>➕ Add Employee</button>
        )}
      </div>

      <div className="filters-section">
        <input
          type="text"
          placeholder="🔍 Search by name"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="filter-input"
        />
        <input
          type="text"
          placeholder="🏷️ Filter by department"
          value={departmentFilter}
          onChange={(e) => setDepartmentFilter(e.target.value)}
          className="filter-input"
        />
      </div>

      <div className="employees-table-container">
        {loading ? (
          <div className="loading">⏳ Loading employees...</div>
        ) : employees.length === 0 ? (
          <div className="no-employees">📋 No employees found matching your criteria.</div>
        ) : (
          <table className="employees-table">
            <thead> 
              <tr>
                <th>Employee ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Position</th>
                <th>Department</th>
                <th>Status</th>
                {/* Only show Actions column if admin */}
                {role === "admin" && <th>Actions</th>}
              </tr>
            </thead>
            <tbody>
              {employees.map((emp, index) => (
                <tr key={emp.employeeId || index}>
                  <td>{emp.employeeId}</td>
                  <td>{emp.name}</td>
                  <td>{emp.email}</td>
                  <td>{emp.position}</td>
                  <td>{emp.department}</td>
                  <td>{emp.status}</td>
                  {/* Only show Edit/Delete if admin */}
                  {role === "admin" ? (
                    <td>
                      <button className="action-btn" onClick={() => navigate(`/employees/edit/${emp.employeeId}`)}>
                        ✏️ Edit
                      </button>
                      <button className="action-btn delete-btn" onClick={() => handleDelete(emp.employeeId)}>
                        🗑️ Delete
                      </button>
                    </td>
                  ) : null}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default Employees