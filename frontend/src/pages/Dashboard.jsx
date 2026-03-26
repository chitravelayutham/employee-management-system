import { useNavigate, Link } from "react-router-dom"
import { jwtDecode } from "jwt-decode"

function Dashboard() {
  const navigate = useNavigate()
  const token = localStorage.getItem("access_token")
  const user = token ? jwtDecode(token) : null
  const role = user?.role

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>🏢 Employee Management Dashboard</h1>
        <p>Welcome back, {user?.name || 'User'}!</p>
      </div>

      <div className="dashboard-content">
        {role === "admin" && (
          <div className="dashboard-section">
            <h2>👑 Admin Panel</h2>
            <div className="dashboard-cards">
              <Link to="/employees" className="dashboard-card">
                <h3>👥 Manage Employees</h3>
                <p>View, add, edit, and delete employee records</p>
              </Link>
              <div className="dashboard-card">
                <h3>📊 Reports</h3>
                <p>Generate HR reports and analytics</p>
              </div>
              <div className="dashboard-card">
                <h3>⚙️ Settings</h3>
                <p>Configure system settings</p>
              </div>
            </div>
          </div>
        )}

        {role === "employee" && (
          <div className="dashboard-section">
            <h2>👤 Employee Portal</h2>
            <div className="dashboard-cards">
              <div className="dashboard-card">
                <h3>👤 My Profile</h3>
                <p>View and update your personal information</p>
              </div>
              <div className="dashboard-card">
                <h3>📋 My Tasks</h3>
                <p>View assigned tasks and projects</p>
              </div>
              <div className="dashboard-card">
                <h3>📅 Time Tracking</h3>
                <p>Log your work hours</p>
              </div>
            </div>
          </div>
        )}

        <div className="dashboard-section">
          <h2>📈 Quick Stats</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Employees</h3>
              <span className="stat-number">--</span>
            </div>
            <div className="stat-card">
              <h3>Active Projects</h3>
              <span className="stat-number">--</span>
            </div>
            <div className="stat-card">
              <h3>Pending Tasks</h3>
              <span className="stat-number">--</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
