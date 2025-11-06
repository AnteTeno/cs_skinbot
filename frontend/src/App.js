import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate, useLocation } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import Dashboard from './components/Dashboard';
import './App.css';

function Navigation() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, [location]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-brand">
          <img src="/cslogo.png" alt="CS Logo" className="nav-logo" />
          <span className="nav-title">CS Skin Bot</span>
        </div>
        <ul className="nav-links">
          {!isLoggedIn ? (
            <>
              <li>
                <Link to="/login" className={location.pathname === '/login' ? 'active' : ''}>Login</Link>
              </li>
              <li>
                <Link to="/signup" className={location.pathname === '/signup' ? 'active' : ''}>Sign Up</Link>
              </li>
            </>
          ) : (
            <>
              <li>
                <Link to="/dashboard" className={location.pathname === '/dashboard' ? 'active' : ''}>Dashboard</Link>
              </li>
              <li>
                <button onClick={handleLogout} className="logout-btn">Logout</button>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <div className="main-content">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/" element={<Login />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
