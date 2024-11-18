import React, { useState } from 'react';
import '../styles/form-styles.css'; 

function Login() {
  const [username, setUsername] = useState(''); // State for username/email
  const [password, setPassword] = useState(''); // State for password
  const [error, setError] = useState(''); // State for form validation errors

  // Handle input changes
  const handleUsernameChange = (e) => setUsername(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    // Basic validation
    if (!username || !password) {
      setError('Please fill in both fields');
      return;
    }

    // TESTING - Simulate login (you'd make an API call here to validate the credentials)
    if (username === 'user' && password === 'password123') {
      setError('');
      alert('Login Successful!');
      // Redirect user or handle successful login here
    } else {
      setError('Invalid username or password');
    }
  };

  return (
    <div className='container'>
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className="form">
        <div className="inputGroup">
          <label htmlFor="username">Username/Email:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={handleUsernameChange}
            className="input"
            placeholder="Enter your username or email"
          />
        </div>
        <div class='inputGroup'>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
            className="input"
            placeholder="Enter your password"
          />
        </div>
        {error && <div className="error">{error}</div>}
        <button className="button" type="submit">Login</button>
      </form>
      <div>
            <p style={{ color: '#7b8087' }}>Don't have an account?</p>
            <a href="/createaccount">
                <p style={{ color: '#007bff', cursor: 'pointer' }}>Create New Account Here</p>
            </a>
        </div>
    </div>
  );
}

export default Login;
