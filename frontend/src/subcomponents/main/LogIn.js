import React, { useState } from 'react';
import '../styles/form-styles.css'; 
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Login({onUserChange}) {
  const loginUrl = 'http://127.0.0.1:4000/apiv1/login'

  const [username, setUsername] = useState(''); // State for username/email
  const [password, setPassword] = useState(''); // State for password
  const [error, setError] = useState(''); // State for form validation errors

  const navigate = useNavigate(); 

  // Handle input changes
  const handleUsernameChange = (e) => setUsername(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);

  const login = async (user, password) => {
    axios.post(loginUrl, {
      email_or_username: user,
      password: password,
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        console.log(response.data);
        onUserChange(response.data.user_id, response.data.username);
        navigate('/');

      })
      .catch(error => {
        console.error('Error:', error);
        setError('Invalid username or password'); 
      });


    
  };
  

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!username || !password) {
      setError('Please fill in both fields');
      return;
    }

    login(username, password)
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
        <div className='inputGroup'>
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
