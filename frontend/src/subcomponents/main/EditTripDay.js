import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; 
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';  
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons'; 
import '../styles/edit-day-styles.css'

const EditTripDay = ({userServerHost, tripServerHost, userId, tripId, tripDayNum, tripDayDate, onTripDayChange}) => {
  const [tripDay, setTripDay] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formDate, setFormDate] = useState(''); 
  const [location, setLocation] = useState('');
  const [accomodation, setAccomodation] = useState('');
  const [travel, setTravel] = useState('');
  const [activities, setActivites] = useState('');
  const [dining, setDining] = useState('');
  const [notes, setNotes] = useState('');

  const getTripDayUrl = `${tripServerHost}/apiv1/tripDay/${tripId}/${tripDayDate}` 
  const patchTripDayUrl = `${tripServerHost}/apiv1/trip/${tripId}/${tripDayDate}` 

  const navigate = useNavigate();

  const fetchTripDayData = async () => {
    console.log(tripDayDate)
    try {
      const tripDayDataResp = await axios.get(getTripDayUrl);
      console.log(tripDayDataResp.data);
      setTripDay(tripDayDataResp.data);
      setLoading(false);

      // set initial form values
      setFormDate(formatDate(tripDayDate)); 
      setLocation(tripDayDataResp.data.location || '');
      setAccomodation(tripDayDataResp.data.accommodations || '');
      setTravel(tripDayDataResp.data.travel || '');
      setActivites(tripDayDataResp.data.activities || '');
      setDining(tripDayDataResp.data.dining || '');
      setNotes(tripDayDataResp.data.notes || '');

    } catch (err) {
      setError('Failed to fetch trip day data');
      console.error(err);
    } 
  };

  const patchTripDay = async (newDate, newActivities, newAccommodations, newDining, newLocation, newNotes, newTravel) => {
    setLoading(true);
    try {
      const patchResp = axios.patch(patchTripDayUrl,
        {
          accommodations: newAccommodations,
          activities: newActivities,
          date: newDate,
          dining: newDining,
          location: newLocation,
          notes: newNotes,
          travel: newTravel,
          last_updated_by: userId,
        },
        {
          'Content-Type': 'application/json',
        }
      );
      console.log(patchResp.data);

    }catch (err) {
      setError('Failed to fetch trip day data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTripDayData();
  }, []);

  const formatDate = (dateString) => {
        const dateObject = new Date(dateString);
        return dateObject.toISOString().split('T')[0];
    };
  
    const formatDateLong = (dateString) => {
      const dateParts = dateString.split('T')[0];
      const [year, month, day] = dateParts.split('-');
      const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ];
      const monthName = monthNames[parseInt(month, 10) - 1];
      const dayWithoutLeadingZero = parseInt(day, 10);
      return `${monthName} ${dayWithoutLeadingZero}, ${year}`
    };


  const [submittedData, setSubmittedData] = useState(null);
  
  const handleDateChange = (event) => setFormDate(event.target.value); 
  const handleLocationChange = (event) => setLocation(event.target.value);
  const handleAccomodationChange = (event) => setAccomodation(event.target.value);
  const handleTravelChange = (event) => setTravel(event.target.value);
  const handleActivitiesChange = (event) => setActivites(event.target.value);
  const handleDiningChange = (event) => setDining(event.target.value);
  const handleNotesChange = (event) => setNotes(event.target.value);

  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();

    // Create an object with the form data
    const formData = {
        formDate,
      location,
      accomodation,
      travel,
      activities,
      dining,
      notes
    };

    // Save the form data for display
    setSubmittedData(formData);

    patchTripDay(formData.formDate, formData.activities, formData.accomodation, formData.dining, formData.location, formData.notes, formData.travel);

    navigate('/tripDetails');

  };

  if (loading) {
    return <div>Loading Trip Day Details...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="form-container">
      <button
      style={{
        fontSize: '16px',
        backgroundColor: 'transparent', 
        color: 'blue',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
      }}
      onClick={() => navigate("/tripDetails")}
    >
      <FontAwesomeIcon icon={faArrowLeft} style={{ marginRight: '8px' }} />
      Return to Trip Days
    </button>
        <h2>Edit <strong> Day {tripDayNum}</strong>  Details </h2>
        <p>{formatDateLong(tripDayDate)}</p>
      <form onSubmit={handleSubmit} className="trip-day-form">
    {/* Date Picker */}
    <div>
          <label>Date:</label>
          <input
            type="date"
            value={formDate}
            onChange={handleDateChange}
          />
    </div>
    <div>
          <label>Location:</label>
          <textarea
            value={location}
            onChange={handleLocationChange}
          />
        </div>
      <div>
          <label>Accommodations:</label>
          <textarea
            value={accomodation}
            onChange={handleAccomodationChange}
          />
        </div>

        <div>
          <label>Travel:</label>
          <textarea
            value={travel}
            onChange={handleTravelChange}
          />
        </div>

        <div>
          <label>Dining:</label>
          <textarea
            value={dining}
            onChange={handleDiningChange}
          />
        </div>

        <div>
          <label>Activities:</label>
          <textarea
            value={activities}
            onChange={handleActivitiesChange}
          />
        </div>

        <div>
          <label>Additional Notes:</label>
          <textarea
            value={notes}
            onChange={handleNotesChange}
          />
        </div>

        <button type="submit">Submit</button>
      </form>

      {/* Display the submitted data after submission */}
      {submittedData && (
        <div>
          <h3>Successfully Saved Day {tripDayNum} Information:</h3>
          <p><strong>Date:</strong> {submittedData.formDate }</p>
          <p><strong>Location:</strong> {submittedData.location}</p>
          <p><strong>Accommodations:</strong> {submittedData.accomodation}</p>
          <p><strong>Travel:</strong> {submittedData.travel}</p>
          <p><strong>Dining:</strong> {submittedData.dining}</p>
          <p><strong>Activities:</strong> {submittedData.activities}</p>
          <p><strong>Notes:</strong> {submittedData.notes}</p>
        </div>
      )}
    </div>
  );
};

export default EditTripDay;
