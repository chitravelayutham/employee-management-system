import React, { useState, useEffect } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { jwtDecode } from "jwt-decode";
import axios from "axios"
import { BASE_URL } from "../api/api"

const EmployeeForm = () => {
  const navigate = useNavigate()
  const { id } = useParams()
  const token = localStorage.getItem("access_token")
  const role = token ? jwtDecode(token).role : null

    
  const [employee, setEmployee] = useState({ employeeId: "", name: "", email: "", department: "", role: "", position: "", status: "Active" })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")

  // Restrict non-admins
  useEffect(() => {
    if (role !== "admin") {
      alert("You are not authorized to access this page")
      navigate("/employees")
    }
  }, [role, navigate])

  // Load employee if editing
  useEffect(() => {
    if (id) {
      setLoading(true)
      axios.get(`${BASE_URL}/employees/${id}`, {  
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(res => {
          setEmployee(prev => ({
            employeeId: "",
            name: "",
            email: "",
            department: "",
            role: "",
            position: "",
            status: "Active",
            ...res.data
          }))
          setLoading(false)
        })
        .catch(err => {
          console.error(err)
          setError("Failed to load employee data")
          setLoading(false)
        })
    }
  }, [id, token])

  const handleChange = e => {
    setEmployee({ ...employee, [e.target.name]: e.target.value })
    setError("")
    setSuccess("")
  }

  const handleSubmit = e => {
    e.preventDefault()
    setLoading(true)
    setError("")
    setSuccess("")

    const apiCall = id
      ? axios.put(`${BASE_URL}/employees/${id}`, employee, { headers: { Authorization: `Bearer ${token}` } })
      : axios.post(`${BASE_URL}/employees/employee`, employee, { headers: { Authorization: `Bearer ${token}` } })

    apiCall
      .then(() => {
        setSuccess(id ? "Employee updated successfully!" : "Employee created successfully!")
        setLoading(false)
        setTimeout(() => navigate("/employees"), 1500)
      })
      .catch(err => {
        console.error(err)
        let msg = "An error occurred";
        if (err.response?.data?.detail) {
          msg = typeof err.response.data.detail === "string" ? err.response.data.detail : JSON.stringify(err.response.data.detail);
        } else if (err.message) {
          msg = err.message;
        }
        setError(msg)
        setLoading(false)
      })
  }

  return (
    <div className="employee-form-container">
      <div className="employee-form-header">
        <h1>{id ? "✏️ Edit Employee" : "➕ Add New Employee"}</h1>
      </div>

      <form className="employee-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label" htmlFor="employeeId">Employee ID</label>
          <input
            type="text"
            id="employeeId"
            name="employeeId"
            value={employee.employeeId}
            onChange={handleChange}
            className="form-input"
            required
            placeholder="Enter employee ID"
          />
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="name">Full Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={employee.name}
            onChange={handleChange}
            className="form-input"
            required
            placeholder="Enter full name"
          />
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="email">Email Address</label>
          <input
            type="email"
            id="email"
            name="email"
            value={employee.email}
            onChange={handleChange}
            className="form-input"
            required
            placeholder="Enter email address"
          />
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="department">Department</label>
          <input
            type="text"
            id="department"
            name="department"
            value={employee.department}
            onChange={handleChange}
            className="form-input"
            required
            placeholder="Enter department"
          />
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="position">Position</label>
          <input
            type="text"
            id="position"
            name="position"
            value={employee.position}
            onChange={handleChange}
            className="form-input"
            required
            placeholder="Enter position (e.g., employee, manager, admin)"
          />
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="status">Status</label>
          <select
            id="status"
            name="status"
            value={employee.status}
            onChange={handleChange}
            className="form-input"
            required
          >
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
            <option value="On-boarding">On-boarding</option>
          </select>
        </div>

        {error && <div className="form-error">❌ {error}</div>}
        {success && <div className="form-success">✅ {success}</div>}

        <div className="form-actions">
          <button type="button" className="cancel-btn" onClick={() => navigate("/employees")}>
            Cancel
          </button>
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? "⏳ Saving..." : (id ? "💾 Update Employee" : "Create Employee")}
          </button>
        </div>
      </form>
    </div>
  )
}

export default EmployeeForm