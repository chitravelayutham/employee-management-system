
import { useState } from "react"
import API from "../api/api"
import { useNavigate, Link } from "react-router-dom"
import logo from "../assets/logo.png"


function Login() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const navigate = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")

    try {
      const res = await API.post("/auth/login", {
        username,
        password
      })

      console.log(res.data);
      localStorage.setItem("access_token", res.data.access_token)
      navigate("/dashboard")
    } catch (err) {
      setError("Invalid username or password")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
         <div className="flex justify-start mb-6">
                 <img src={logo} alt="Logo" className="h-16 w-16 object-contain" width={300} height={300} />
               </div>
       
               <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">
                 Employee Management System
               </h2>

        <form className="auth-form" onSubmit={handleLogin}>
          <div className="form-group">
            <label className="form-label" htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-input"
              required
            />
          </div>

          {error && <div className="form-error">❌ {error}</div>}

          <button type="submit" className="auth-btn" disabled={loading}>
            {loading ? "⏳ Signing in..." : "🚀 Sign In"}
          </button>
        </form>

        <div className="auth-footer">
          <p>Don't have an account? <Link to="/register">Create one here</Link></p>
          <p><Link to="/forgot-password">Forgot password?</Link></p>
        </div>
      </div>
    </div>
  )
}

export default Login