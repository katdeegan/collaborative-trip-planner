import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // React Router hook to navigate
import '../styles/edit-day-styles.css'
import axios from 'axios'; 

const CreateTrip = ({userId}) => {
  // States to store form data
  const [tripName, setTripName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  // Use the navigate hook for redirecting
  const navigate = useNavigate();

  const createTripAndAddUser = async (tripName, startDate, endDate) => {
    const createTripUrl = 'http://127.0.0.1:2000/apiv1/trip'; 
    const addUserUrl = 'http://127.0.0.1:4000/apiv1/tripGroup'; 

    const tripData = { trip_name: tripName, start_date: startDate, end_date: endDate};  

    try {
      const createTripResp = await axios.post(createTripUrl, tripData, {
        headers: { 'Content-Type': 'application/json' },
      });

      console.log('Trip created response:', createTripResp.data);

      console.log(createTripResp.data[0].trip_id)

      const tripUserData = { user_id: userId, trip_id: createTripResp.data[0].trip_id };

      const addUserResp = await axios.post(addUserUrl, tripUserData, {
        headers: { 'Content-Type': 'application/json' },
      });

      console.log('Adding user to trip response:', addUserResp.data);

      setResponse({createTripResponse: createTripResp.data, addUserResponse: addUserResp.data});
      } catch (err) {
        setError(err.message)
      }
  };

  // Form submit handler
  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = {
        tripName,
        startDate,
        endDate
    };

    createTripAndAddUser(tripName, startDate, endDate);

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