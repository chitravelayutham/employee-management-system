import { useNavigate, Link } from "react-router-dom"
import { jwtDecode } from "jwt-decode"
import { useEffect, useState } from "react"
import { PieChart, Pie, Tooltip, Legend, ResponsiveContainer } from "recharts"
import axios from "axios"

function Dashboard() {
  const navigate = useNavigate()

  const token = localStorage.getItem("access_token")

  let user = null
  try {
    user = token ? jwtDecode(token) : null
  } catch {
    user = null
  }

  const role = user?.role

  const [deptData, setDeptData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    let isMounted = true

    axios.get("http://127.0.0.1:8000/employees", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => {
        if (!isMounted) return

        const employees = Array.isArray(res.data) ? res.data : []

        const deptMap = {}
        employees.forEach(emp => {
          const dept = emp.department || "Unknown"
          deptMap[dept] = (deptMap[dept] || 0) + 1
        })

        // Add color directly into data (replaces <Cell />)
        const COLORS = [
          "#0088FE", "#00C49F", "#FFBB28", "#FF8042",
          "#A28CFE", "#FF6699", "#33CC99", "#FF4444"
        ]

        const chartData = Object.entries(deptMap).map(
          ([name, value], index) => ({
            name,
            value,
            fill: COLORS[index % COLORS.length]
          })
        )

        setDeptData(chartData)
        setLoading(false)
      })
      .catch(() => {
        if (!isMounted) return
        setError("Could not fetch employees")
        setLoading(false)
      })

    return () => {
      isMounted = false
    }
  }, [token])

  const totalEmployees = deptData.reduce((sum, d) => sum + d.value, 0)

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>🏢 Employee Management Dashboard</h1>
        <p>Welcome back, {user?.name || "User"}!</p>
      </div>

      <div className="dashboard-content">

        {/* ADMIN OR USER */}
           <div className="dashboard-section">
              <div className="dashboard-cards">
              <Link to="/employees" className="dashboard-card">
                <h3>👥 Manage Employees</h3>
                <p>View, add, edit, and delete employee records</p>
              </Link>
            </div>
          </div>
      

        {/* EMPLOYEE */}
       {/*  {role === "admin" && (
          <div className="dashboard-section">
            <h2>👤 Employee Portal</h2>
            <div className="dashboard-cards">
              <div className="dashboard-card">
                <h3>👤 My Profile</h3>
              </div>
            </div>
          </div>
        )} */}

        {/* STATS */}
        <div className="dashboard-section">
          <h2>📈 Quick Stats</h2>

          {loading ? (
            <p>Loading stats...</p>
          ) : (
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Total Employees</h3>
                <span className="stat-number">{totalEmployees}</span>
              </div>
            </div>
          )}

          {/* CHART */}
          <div style={{ width: "100%", maxWidth: 500, margin: "2rem auto" }}>
            <h3 style={{ textAlign: "center" }}>
              Employees by Department
            </h3>

            {loading ? (
              <div>Loading chart...</div>
            ) : error ? (
              <div style={{ color: "red" }}>{error}</div>
            ) : deptData.length === 0 ? (
              <div>No employee data available.</div>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={deptData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label
                  />
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>

        </div>
      </div>
    </div>
  )
}

export default Dashboard