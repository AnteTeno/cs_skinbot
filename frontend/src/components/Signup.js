import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

function Signup() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!username || !email || !password) {
      setError('Please fill in all fields');
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      if (response.ok) {
        setSuccess(true);
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      } else {
        const errorData = await response.json().catch(() => ({}));
        setError(errorData.detail || 'Signup failed. Username or email may already exist.');
      }
    } catch (error) {
      setError('Connection error. Please check if the server is running.');
      console.error('Error during signup:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Sign Up</h2>
      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}
      {success && (
        <div className="alert alert-success">
          Account created successfully! Redirecting to login...
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Choose a username"
            disabled={loading || success}
          />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            disabled={loading || success}
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Create a password (min 6 characters)"
            disabled={loading || success}
          />
        </div>
        <button type="submit" className="form-btn" disabled={loading || success}>
          {loading ? 'Creating account...' : success ? 'Success!' : 'Sign Up'}
        </button>
      </form>
      <div className="form-link">
        Already have an account? <Link to="/login">Login here</Link>
      </div>
    </div>
  );
}

export default Signup;
