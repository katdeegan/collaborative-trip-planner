import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/form-styles.css'; 

function CreateAccount({onUserChange}) {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
      });
      const [errors, setErrors] = useState({});
      const [isSubmitting, setIsSubmitting] = useState(false);

      const [response, setResponse] = useState(null);
      const [error, setError] = useState(null); // errors for POST request

      const navigate = useNavigate(); 
    
      // Handle form input changes
      const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
          ...prevData,
          [name]: value,
        }));
      };
    
      // Validate the form fields
      const validate = () => {
        const errors = {};
        if (!formData.username) errors.username = 'Username is required';
        if (!formData.email) errors.email = 'Email is required';
        if (!formData.password) errors.password = 'Password is required';
        if (formData.password !== formData.confirmPassword) {
            errors.confirmPassword = 'Passwords do not match';
          }
          return errors;
        };
    
      // Handle form submission
    const handleSubmit = async(e) => {
        e.preventDefault();
        const formErrors = validate();
        if (Object.keys(formErrors).length === 0) {
          setIsSubmitting(true);
          console.log('Create Account Data:', formData);

          const createUserUrl = 'http://127.0.0.1:4000/apiv1/user';

          const newUserData = {
            username: formData.username,
            email: formData.email,
            password: formData.password,
          };

          const config = {
            headers: {
              'Content-Type': 'application/json',
            },
          };

          try {
            const response = await axios.post(createUserUrl, newUserData, config)
            setResponse(response.data)
            console.log('New user created.');
            onUserChange(response.data[0].user_id, response.data[0].username);
            navigate('/'); 
          } catch (err) {
            setError(err.message)
          }

        } else {
          setErrors(formErrors);
        }
    };


  return (
    <div className='container'>
      <h2>Create New Account</h2>
      <form onSubmit={handleSubmit} className="form">
        <div className="inputGroup">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className="input"
            placeholder="Enter your username"
            required
          />
          {errors.username && <p className="error">{errors.username}</p>}
        </div>
        <div className="inputGroup">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="input"
            placeholder="Enter your email"
            required
          />
          {errors.email && <p className="error">{errors.email}</p>}
        </div>
        <div className='inputGroup'>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="input"
            placeholder="Enter your password"
            required
          />
          {errors.password && <p className="error">{errors.password}</p>}
        </div>
        <div className="inputGroup">
          <label htmlFor="confirmPassword">Confirm Password:</label>
          <input
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            className="input"
            placeholder="Re-enter your password"
            required
          />
        
          {errors.confirmPassword && <p className="error">{errors.confirmPassword}</p>}
        </div>
        <button className="button" type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>
      <div>
            <p style={{ color: '#7b8087' }}>Already have an account?</p>
            <a href="/login">
                <p style={{ color: '#007bff', cursor: 'pointer' }}>Login Here</p>
            </a>
        </div>
    </div>
  );
}

export default CreateAccount;
