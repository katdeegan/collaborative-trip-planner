// TO dO - update with proper logic for trip DB
import React, { Component } from 'react';
import { useParams } from 'react-router-dom';
import { Table } from 'react-bootstrap';
import { format } from 'date-fns';
import { Link } from 'react-router-dom';
import axios from 'axios'; // library for HTTP requests to backend API
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';  
import { faPen } from '@fortawesome/free-solid-svg-icons'; 
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/form-styles.css'; 

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

    const { id } = useParams();
    
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return format(date, 'MMMM d, yyyy');
    };

    return (
    <div >
      <h1>{tripOverviewData[0].name}</h1>
      <h4>{`Trip Dates: ${formatDate(tripOverviewData[0].startDate)} to ${formatDate(tripOverviewData[0].endDate)}`}</h4>
      {/* Add other trip details here */}

      <div >
        {tripDataByDay.map((item, idx) => (
            <div className='trip-day-div'>
            <div className='two-item-grid-container'>
                <h1>Day {idx+1}: {item.location}</h1>
                <Link to={`/editTripDay/${item.id}`}>
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
            </div>
            ))}
      </div>
    </div>
    );
};


export default TripDetail;

