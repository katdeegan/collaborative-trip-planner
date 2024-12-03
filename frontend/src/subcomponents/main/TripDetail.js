// TO dO - update with proper logic for trip DB
import React, { Component, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Button, Table } from 'react-bootstrap';
import { format } from 'date-fns';
import { Link } from 'react-router-dom';
import axios from 'axios'; // library for HTTP requests to backend API
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';  
import { faPen, faPlus, faTimes  } from '@fortawesome/free-solid-svg-icons'; 
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/home.css'; 
import ChangeTripDatesModal from './ChangeTripDatesModal';

const TripDetail = () => {

    const tripOverviewData = [
        { id: 1, name: 'My Trip', startDate: '2024-11-01T10:00:00Z', endDate: '2024-11-04T10:00:00Z' }
      ];

    // TO do - make sure data is ordered by date
    const tripDataByDay = [
        { id: 1, tripId: 1, date: '2024-11-01T10:00:00Z', location: 'Madrid', accomodation: 'Madrid Motel - 100 Madrid St',
            travel: 'Ryan Air flight 200', activities: 'Flamenco show', dining: '', notes: 'Day 1'
          },
          { id: 4, tripId: 1, date: '2024-11-02T10:00:00Z', location: 'Madrid', accomodation: 'Madrid Motel - 100 Madrid St',
            travel: '', activities: 'Flamenco show', dining: '', notes: 'Day 2'
          },
          { id: 7, tripId: 1, date: '2024-11-03T10:00:00Z', location: 'Madrid', accomodation: 'Madrid Motel - 100 Madrid St',
            travel: 'bus', activities: 'day trip', dining: 'tapas!', notes: 'Day 3'
          },
          { id: 10, tripId: 1, date: '2024-11-04T10:00:00Z', location: 'Madrid', accomodation: 'Madrid Motel - 100 Madrid St',
            travel: 'Ryan Air flight 755', activities: 'explore!', dining: 'mischlin', notes: 'Day 4'
          }

      ];

    const tripMemberData = [{username: "kat"}, {username: "sierra"}]

    const { id } = useParams();

    const [isModalOpen, setIsModalOpen] = useState(false);
    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);
    const [startDate, setStartDate] = useState(tripOverviewData[0].startDate);
    const [endDate, setEndDate] = useState(tripOverviewData[0].endDate);

    // Do we need?? this is for Add trip day
    const [loading, setLoading] = useState(false);
    
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return format(date, 'MMMM d, yyyy');
    };

    const handleSave = (newStartDate, newEndDate) => {
        setStartDate(newStartDate);
        setEndDate(newEndDate);
        console.log('Saved dates:', newStartDate, newEndDate);
      };

      const deleteTripDay = async () => { 
        console.log("Deleting trip day...")
        const userConfirmed = window.confirm("Are you sure you want to delete this trip day?");
        if (userConfirmed) {
          // Proceed with the action if user clicks OK
          console.log("Action confirmed!");
          // You can execute any action here, such as calling an API or executing a function
        } else {
          // Action is canceled if user clicks Cancel
          console.log("Action canceled.");
        }

      };
    
  // TO-DO: Function to add a new trip day
  const addTripDay = async () => {
    console.log("Adding trip day...")
    setLoading(true);

    // Create the payload to send to the backend API
        const requestBody = {
          };

          try {
            // Call the backend API (Replace with your actual backend URL)
            const response = await fetch('http://localhost:5000/api/database-operation', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(requestBody),
            });
      
            const data = await response.json();

      if (response.ok) {
        // If the operation is successful, log the success message
        console.log(data.message);
        alert(data.message); // Show success message to user
      } else {
        // If the operation failed, log the error message
        console.log(data.message);
        alert(data.message); // Show error message to user
      }
      // Reload the page after the operation is completed
      window.location.reload();

    } catch (error) {
        // Handle any errors that occur during the fetch request
        console.error('Error executing database operation:', error);
        alert('An error occurred during the database operation.');
      } finally {
        setLoading(false);
      }
  };

    return (
    <div className = 'page-container' >
      <h1>{tripOverviewData[0].name}</h1>
      <div>
        <div className='two-item-grid-container-closer'>
      <p >{`Trip Dates: ${formatDate(tripOverviewData[0].startDate)} to ${formatDate(tripOverviewData[0].endDate)}`}</p>
      <div style={{marginBottom: 16 + 'px'}}>
      <button className="edit-btn" onClick={openModal}>
       <FontAwesomeIcon icon={faPen} />
       </button>
       </div>
       </div>

        {/* Modal with editable date fields */}
        <ChangeTripDatesModal
        isOpen={isModalOpen}
        onClose={closeModal}
        startDate={startDate}
        endDate={endDate}
        onSave={handleSave}
        />
        </div>

        <div> 
            <div className="two-item-grid-container-closer">
            <h4>Trip Members:</h4>
            <div style={{marginBottom: 16 + 'px'}}>
            <Link className="edit-btn" to={`/editTripMembers/${tripOverviewData[0].id}}`}>
                <FontAwesomeIcon icon={faPen} /> 
            </Link>
            </div>
            </div>
            <ol>
                {tripMemberData.map((user, index) => (
                <li key={index}>{user.username}</li> // Map each username into a <li>
                ))}
             </ol>
             
        </div>

      <div >
        {tripDataByDay.map((item, idx) => (
            <div className='trip-day-div'>
            <div className='two-item-grid-container'>
                <h1>Day {idx+1}: {item.location}</h1>
                <Link className="edit-btn" to={`/editTripDay/${idx+1}/${item.tripId}/${item.date}`}>
                <FontAwesomeIcon icon={faPen} /> 
                </Link>
            </div>
            <p>{formatDate(item.date)}</p>
            <Table striped bordered hover responsive className="custom-table">
                <thead>
                    <tr>
                    <th>Accommodations</th>
                    <th>Travel</th>
                    <th>Dining</th>
                    <th>Activities</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{item.accomodation}</td>
                        <td>
                        {item.travel}
                        </td>
                        <td>
                        {item.dining}
                        </td>
                        <td>{item.activities}</td>
                    </tr>
                </tbody>
            </Table>
            <h5>Additional Notes:</h5>
            <p>{item.notes}</p>
            <button onClick={deleteTripDay}>
            <FontAwesomeIcon icon={faTimes} style={{ marginRight: '8px' }} />
            Delete Trip Day
            </button>
            </div>
            ))}
      </div>
      <div>
      <button onClick={addTripDay}>
       <FontAwesomeIcon icon={faPlus} style={{ marginRight: '8px' }} />
                Add Trip Day
    </button>

            </div>
    </div>
    );
};


export default TripDetail;

