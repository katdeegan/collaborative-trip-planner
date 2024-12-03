import React, { useState } from 'react';
import '../styles/form-styles.css'; 
<<<<<<< HEAD
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Login({onUserChange}) {
  const loginUrl = 'http://127.0.0.1:4000/apiv1/login'

=======

function Login() {
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a
  const [username, setUsername] = useState(''); // State for username/email
  const [password, setPassword] = useState(''); // State for password
  const [error, setError] = useState(''); // State for form validation errors

<<<<<<< HEAD
  const navigate = useNavigate(); 

=======
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a
  // Handle input changes
  const handleUsernameChange = (e) => setUsername(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);

<<<<<<< HEAD
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

=======
  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    // Basic validation
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a
    if (!username || !password) {
      setError('Please fill in both fields');
      return;
    }

<<<<<<< HEAD
    login(username, password)
=======
    // TESTING - Simulate login (you'd make an API call here to validate the credentials)
    if (username === 'user' && password === 'password123') {
      setError('');
      alert('Login Successful!');
      // Redirect user or handle successful login here
    } else {
      setError('Invalid username or password');
    }
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a
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
<<<<<<< HEAD
        <div className='inputGroup'>
=======
        <div class='inputGroup'>
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a
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
