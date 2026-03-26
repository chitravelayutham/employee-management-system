import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="home-container">
      <div className="hero-section">
        <h1>Welcome to Employee Management System</h1>
       
        <div className="hero-buttons">
          <Link to="/login" className="btn-primary">Get Started</Link>
          <Link to="/register" className="btn-secondary">Sign Up</Link>
        </div>
      </div>
      </div>

      
  );
};

export default Home;