import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { format } from 'date-fns';
import '../styles/edit-day-styles.css'

const EditTripDay = () => {
    const { dayNum, tripId, date } = useParams();

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return format(date, 'MMMM d, yyyy');
    };
// GET request to retrieve data by trip_id + date
const tripDataByDay = [
    {tripId: 1, date: '2024-11-01T10:00:00Z', location: 'Madrid', accomodation: 'Madrid Motel - 100 Madrid St',
        travel: 'Ryan Air flight 200', activities: 'Flamenco show', dining: '', notes: 'Day 1'
      }

  ];

  // State hooks to store form field values
  const dateObject = new Date(tripDataByDay[0].date)
  const formattedDate = dateObject.toISOString().split('T')[0];

  const [formDate, setFormDate] = useState(formattedDate || ''); 
  const [location, setLocation] = useState(tripDataByDay[0].location || '');
  const [accomodation, setAccomodation] = useState(tripDataByDay[0].accomodation || '');
  const [travel, setTravel] = useState(tripDataByDay[0].travel || '');
  const [activities, setActivites] = useState(tripDataByDay[0].activities || '');
  const [dining, setDining] = useState(tripDataByDay[0].dining || '');
  const [notes, setNotes] = useState(tripDataByDay[0].notes || '');

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

  };

  return (
    <div className="form-container">
        <h2>Edit <strong> Day {dayNum}</strong>  Details </h2>
        <p>{formatDate(date)}</p>

      {/* Form to collect name, email, and message */}
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
          <h3>Successfully Saved Day {dayNum} Information:</h3>
          <p><strong>Date:</strong> {submittedData.formDate}</p>
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
