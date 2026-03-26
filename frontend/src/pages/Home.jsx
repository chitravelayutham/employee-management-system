
import React from "react";
import { Link } from "react-router-dom";


const Home = () => {
  return (
    <div className="home-container" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="hero-section" style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div className="hero-buttons" style={{ display: 'flex', gap: '2rem' }}>
          <Link to="/login" className="btn-primary">Get Started</Link>
          <Link to="/register" className="btn-secondary">Sign Up</Link>
        </div>
      </div>
    </div>
  );
};

export default Home;