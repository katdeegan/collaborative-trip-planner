// TO dO - update with proper logic for trip DB
import React, { useState, useEffect } from 'react';
import { Button, Table } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios'; // library for HTTP requests to backend API
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';  
import { faPen, faPlus, faTimes, faArrowLeft } from '@fortawesome/free-solid-svg-icons'; 
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/home.css'; 
import ChangeTripDatesModal from './ChangeTripDatesModal';

const TripDetail = ({userServerHost, tripServerHost, userId, tripId, onTripChange, onTripDayChange}) => {

  const navigate = useNavigate();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const [tripOverview, setTripOverview] = useState(null);
  const [tripDays, setTripDays] = useState(null);
  const [tripMembers, setTripMembers] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [loadingDelete, setLoadingDelete] = useState(false);
  const [highDate, setHighDate] = useState(null);
  const [lowDate, setLowDate] = useState(null);
  const [addTripDayResponseData, setAddTripDayResponseData] = useState(null);

  const tripOverviewUrl = `${tripServerHost}/apiv1/trip/${tripId}`
  const tripDaysUrl = `${tripServerHost}/apiv1/tripDays/${tripId}`
  const tripMembersUrl = `${userServerHost}/apiv1/tripUsers/${tripId}`
  const deleteTripDayUrl = `${tripServerHost}/apiv1/deleteTripDay/`
  const addTripDayUrl = `${tripServerHost}/apiv1/tripDay`

  const formatDate = (dateString) => {
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

  const getNextDay = (dateString) => {
    const date = new Date(dateString);

    // Add one day to the date
    date.setDate(date.getDate() + 1);

    // Format the new date back to 'YYYY-MM-DD'
    const nextDay = date.toISOString().split('T')[0]; // 'YYYY-MM-DD'

    return nextDay;
  }

  const handleSave = (newStartDate, newEndDate) => {
    setStartDate(newStartDate);
    setEndDate(newEndDate);
    console.log('Saved dates:', newStartDate, newEndDate);
  };

  const fetchTripData = async () => {
    try {
      const [tripOverviewResp, tripMemberResp, tripDaysResp] = await Promise.all([
        axios.get(tripOverviewUrl), 
        axios.get(tripMembersUrl), 
        axios.get(tripDaysUrl), 
      ]);

      // Sort the trip days by date
      const sortedTripDays = tripDaysResp.data.tripDays.sort((a, b) => {
        const dateA = new Date(a.date); 
        const dateB = new Date(b.date); 
        return dateA - dateB;           
      });

      console.log(sortedTripDays);

      setTripOverview(tripOverviewResp.data);
      setTripMembers(tripMemberResp.data);
      setTripDays(sortedTripDays);

      if (sortedTripDays.length > 0) {
        const earliestDate = sortedTripDays[0].date;
        const latestDate = sortedTripDays[sortedTripDays.length - 1].date; 
        setLowDate(earliestDate);
        setHighDate(latestDate);
        console.log("First trip day: "+earliestDate)
        console.log("Last trip day: "+latestDate)
      }



    } catch (err) {
      setError('Failed to fetch trip data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTripData();
  }, []);

  const deleteTripDay = async (tripDate, tripId) => { 
    console.log("Deleting trip day...")
    const userConfirmed = window.confirm("Are you sure you want to delete this trip day?");
    if (userConfirmed) {
      setLoadingDelete(true);
      try {
        const deleteResp = await axios.delete(deleteTripDayUrl + `${tripId}/${tripDate}`);

        if (deleteResp.status === 200) {
          console.log(`Trip day ${tripDate} deleted from trip ${tripId}`);
          fetchTripData();
        }
      } catch (error) {
        console.error("Error deleting the trip day:", error);
      } finally {
        setLoadingDelete(false);
      }
    } else {
      console.log("Action canceled.");
    }

  };

  const addTripDay = async (tripId, tripDate) => {
      console.log("Adding trip day...")
      setLoading(true); 
      setError(null); 
      try {
        const postData = {trip_id: tripId, date: tripDate}
  
        const response = await axios.post(addTripDayUrl, postData);
        setAddTripDayResponseData(response.data);
      } catch (err) {
        setError('An error occurred while trying to add day to the trip.');
      } finally {
        setLoading(false); 
        fetchTripData();
      }
    };
  

  // Render the UI
  if (loading) {
    return <div>Loading Trip Details...</div>;
  }

  if (loadingDelete) {
    return <div>Deleting trip day...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }
    return (
    <div className = 'page-container' >
      <div className='two-item-grid-container' >
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
      onClick={() => navigate("/")}
    >
      <FontAwesomeIcon icon={faArrowLeft} style={{ marginRight: '8px' }} />
      Return to Home
    </button>
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
      onClick={() => navigate("/uploadTripDocument")}
    > Upload Document </button>
    </div>
      <h1>{tripOverview.trip_name}</h1>
      
      <div>
        <div className='two-item-grid-container-closer'>
      <p ><strong>Dates: </strong>{`${formatDate(lowDate)} to ${formatDate(highDate)}`}</p>
      <div style={{marginBottom: 16 + 'px'}}>
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
            <Link className="edit-btn" to={`/editTripMembers/${tripId}}`}>
                <FontAwesomeIcon icon={faPen} /> 
            </Link>
            </div>
            </div>
            <ol>
                {tripMembers.map((user) => (
                <li key={user.user_id}>{user.username}</li> // Map each username into a <li>
                ))}
             </ol>
             
        </div>

      <div >
        {tripDays.map((item, idx) => (
            <div className='trip-day-div'>
            <div className='two-item-grid-container'>
                <h1>Day {idx+1}: {item.location}</h1>
                <Link className="edit-btn" to={`/editTripDay`} onClick={() => onTripDayChange(idx+1, item.date)}>
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
                        <td>{item.accommodations}</td>
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
            <button onClick={() => deleteTripDay(item.date, tripId)}>
            <FontAwesomeIcon icon={faTimes} style={{ marginRight: '8px' }} />
            Delete Trip Day
            </button>
            </div>
            ))}
      </div>
      <div>
      <button onClick={() => addTripDay(tripId, getNextDay(highDate))}>
       <FontAwesomeIcon icon={faPlus} style={{ marginRight: '8px' }} />
                Add Trip Day
    </button>

            </div>
    </div>
    );
};


export default TripDetail;

