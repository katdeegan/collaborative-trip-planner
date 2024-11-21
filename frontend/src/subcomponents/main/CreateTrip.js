import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // React Router hook to navigate
import '../styles/edit-day-styles.css'

const CreateTrip = () => {
  // States to store form data
  const [tripName, setTripName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  // Use the navigate hook for redirecting
  const navigate = useNavigate();

  // Form submit handler
  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = {
        tripName,
        startDate,
        endDate
    };


    // Display an alert on form submission
    const alertMessage = `Trip "${tripName}" created!\nStart Date: ${startDate}\nEnd Date: ${endDate}`;
    alert(alertMessage);

    // After the alert is dismissed, redirect to another page (e.g., home page)
    navigate('/');
  };

    return (
        <div>
          <h2>Create New Trip</h2>
          <form onSubmit={handleSubmit}>
            <div>
              <label htmlFor="textField">Trip Name:</label>
              <input
                type="text"
                id="textField"
                value={tripName}
                onChange={(e) => setTripName(e.target.value)}
                required
              />
            </div>
    
            <div>
              <label htmlFor="startDate">Start Date:</label>
              <input
                type="date"
                id="startDate"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                required
              />
            </div>
    
            <div>
              <label htmlFor="endDate">End Date:</label>
              <input
                type="date"
                id="endDate"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                required
              />
            </div>
    
            <div>
              <button type="submit">Submit</button>
            </div>
          </form>
        </div>
      );
    };


export default CreateTrip;