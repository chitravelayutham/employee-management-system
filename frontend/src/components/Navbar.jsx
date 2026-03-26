import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const Navbar = () => {
  const navigate = useNavigate();

  // Get token from localStorage
  const token = localStorage.getItem("access_token");
  let role = null;

  if (token) {
    try {
      const payload = jwtDecode(token);
      const now = Date.now() / 1000; // current time in seconds

      if (payload.exp && payload.exp < now) {
        // Token expired
        localStorage.removeItem("access_token");
      } else {
        role = payload.role;
      }
    } catch (err) {
      console.error("Invalid token", err);
      localStorage.removeItem("access_token");
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("access_token");  
    navigate("/"); // Redirect to login page
  };

  return (
    <nav className="navbar">
      <div
        className="nav-links"
        style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}
      >
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        {/* Common links */}
        <span><Link to="/home">Home</Link></span>
        

        {/* Role-based links */}
       
            <span><Link to="/dashboard">Dashboard</Link></span>
            <span><Link to="/reports">Reports</Link></span>
            <span><Link to="/profile">My Profile</Link></span>
           
       
        </div>
        {/* Logout button aligned right */}
        {token && (
          <span>
            <button onClick={handleLogout}>Logout</button>
          </span>
        )}
      </div>
    </nav>
  );
};

export default Navbar;