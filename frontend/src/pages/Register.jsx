import { useState } from "react"
import API from "../api/api"
import { useNavigate, Link } from "react-router-dom"

function Register() {
  const [username, setName] = useState("")
  const [role, setRole] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const navigate = useNavigate()

  const register = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")

    if (password.length < 8) {
      setError("Password must be at least 8 characters long")
      setLoading(false)
      return
    }
    if (!username.trim() || !email.trim() || !role.trim()) {
      setError("All fields are required")
      setLoading(false)
      return
    }

    try {
      await API.post("/auth/register", {
        email,
        username,
        password,
        role
      })

      alert("User created successfully!")
      navigate("/login")
    } catch (error) {
      console.error("Registration error:", error.response?.data)
      setError("Registration failed: " + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>📝 Create Account</h2>
          <p>Join Employee Management System and get started managing your team!</p>
        </div>

        <form className="auth-form" onSubmit={register}>
          <div className="form-group">
            <label className="form-label" htmlFor="name">Full Name</label>
            <input
              type="text"
              id="name"
              placeholder="Enter your full name"
              value={username}
              onChange={(e) => setName(e.target.value)}
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Create a strong password (min 8 chars)"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="role">Role</label>
            <select
              id="role"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="form-input"
              required
            >
              <option value="">Select role</option>
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          {error && <div className="form-error">❌ {error}</div>}

          <button type="submit" className="auth-btn" disabled={loading}>
            {loading ? "⏳ Creating Account..." : "🎉 Create Account"}
          </button>
        </form>

        <div className="auth-footer">
          <p>Already have an account? <Link to="/">Sign in here</Link></p>
        </div>
      </div>
    </div>
  )
}

export default Register