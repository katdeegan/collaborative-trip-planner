/* Home page after user logs in. User can view list of all trip
groups they are a member of, and create a new trip group. */

import React, { useState, useEffect } from "react";
import { Table } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight, faPlus, faSyncAlt } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';
import Title from './Title';
import '../styles/form-styles.css'; 
import axios from 'axios';



function Home({username, userId, onUserChange, tripId, onTripChange}) {

  const handleLogOut = () => {
        console.log('Loggin user out...');
        console.log(`Current user: ${userId} ${username}`)
        onUserChange('','')
      };
    

  return (
            <>
            <div className='two-item-grid-container'>
              <h4>Welcome, {username}!</h4>
                <Link to='/login'>
                <button onClick={handleLogOut}>Log Out</button>
                </Link>
            </div>
            <Title/>
            <TripGroupList userId={userId} onTripChange={onTripChange}/>
            <div>
                <Link to='/createtrip'>
                <button style={{ alignItems: 'center', padding: '10px 20px', borderRadius: '5px' }}>
                <FontAwesomeIcon icon={faPlus} style={{ marginRight: '8px' }} />
                New Trip
                </button>
                </Link>
            </div>
            </>
        );
    
}


const TripGroupList = ({userId, onTripChange}) => {
    // retrieve trip list from logged in user
    const [trips, setTrips] = useState(null);
    const [loading, setLoading] = useState(true); 
    const [error, setError] = useState(null); 

    const tripGroupsUrl = `http://127.0.0.1:4000/apiv1/tripGroup/${userId}`
  
    const fetchTrips = async () => {
        try {
          const response = await axios.get(tripGroupsUrl);
          setTrips(response.data); 
          setLoading(false);
        } catch (error) {
          setError(error.message);
          setLoading(false);
        }
      };

    useEffect(() => {
      fetchTrips();
    }, []);

    const handleRefresh = () => {
      fetchTrips();  // Re-fetch trip data
    };

    if (loading) {
      return <div>Retrieving Trips...</div>;
    }
  
    if (error) {
      return <div>Error retrieving trips: {error}</div>;
    }

    if (trips.length === 0) {
      return <div>No trips available.</div>;
    }

        return (
            <Table>
                <thead>
                    <tr>
                      <th>Trip Groups</th>
                      <th><button
        onClick={handleRefresh}
        disabled={loading}
        style={{
          fontSize: '17px',
          backgroundColor: 'transparent',
          border: 'none',
          cursor: loading ? 'not-allowed' : 'pointer',
          padding: '10px',
          color: loading ? '#999' : '#1E90FF',}}
      >
        <FontAwesomeIcon icon={faSyncAlt} spin={loading} />
      </button>
                      </th>
                    </tr>
                </thead>
                <tbody>
                    {trips.map((trip) => (
                        <tr key={trip.trip_id}>
                            <td>{trip.trip_name}</td>
                            <td>
                                <Link to={`/tripDetails`} onClick={() => onTripChange(trip.trip_id)}>
                                    <FontAwesomeIcon icon={faArrowRight} />
                                </Link>
                            </td>
            
                        </tr>
                    ))}
                </tbody>
            </Table>

        )
    
}



export default Home;
