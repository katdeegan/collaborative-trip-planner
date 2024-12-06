// FormPage.js (The form where you select multiple options)
import React, { useState, useEffect } from 'react';
import { useNavigate  } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';  
import { faTimes, faArrowLeft  } from '@fortawesome/free-solid-svg-icons'; 
import axios from 'axios';
import '../styles/add-users-form.css'

const EditTripMembers = ({userServerHost, tripServerHost, tripId}) => {
  const [tripMembers, setTripMembers] = useState(null);
  const [addUserResponseData, setAddUserResponseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadingDelete, setLoadingDelete] = useState(false);
  const [error, setError] = useState(null);

  const [newMember, setNewMember] = useState();
  const handleNewMemberChange = (event) => setNewMember(event.target.value);

  const tripMembersUrl = `${userServerHost}/apiv1/tripUsers/${tripId}`
  const addTripMemberUrl = `${userServerHost}/apiv1/tripGroup`
  const getUserInfoUrl = `${userServerHost}/apiv1/user/`
  const deleteUserFromTripUrl = userServerHost + '/apiv1/deleteTripUser/'

  const navigate = useNavigate();

  const fetchTripMembers = async () => {
    try {
      const tripMemberResp = await axios.get(tripMembersUrl);
      setTripMembers(tripMemberResp.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch trip member data');
      console.error(err);
    } 
  };

  useEffect(() => {
    fetchTripMembers();
  }, []);

  const addTripMember = async(username, tripId) => {
    setLoading(true); 
    setError(null); 
    try {
      const getUserIdResp = await axios.get(getUserInfoUrl+username);

      const userId = getUserIdResp.data.user_id;

      if (!userId) {
        throw new Error('User ID not found in the response');
      }

      console.log('Adding User ' + userId + 'to trip...')

      const postData = {user_id: userId, trip_id: tripId}

      const response = await axios.post(addTripMemberUrl, postData);
      setAddUserResponseData(response.data);
    } catch (err) {
      setError('An error occurred while trying to add user to the trip.');
    } finally {
      setLoading(false); 
      fetchTripMembers();
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    addTripMember(newMember, tripId);
    navigate('/tripDetails');
  };

  const deleteTripMember = async (userId, username, tripId) => { 
    console.log("Deleting trip member...")
    const userConfirmed = window.confirm(`Are you sure you want to delete ${username} from the trip?`);
    if (userConfirmed) {
      setLoadingDelete(true);
      try {
        const deleteResp = await axios.delete(deleteUserFromTripUrl + `${userId}/${tripId}`);

        if (deleteResp.status === 200) {
          console.log(`User ${username} deleted from trip ${tripId}`);
          fetchTripMembers();
        }
      } catch (error) {
        console.error("Error deleting the user:", error);
      } finally {
        setLoadingDelete(false);
      }
    } else {
      console.log("Action canceled.");
    }

  };

  if (loading) {
    return <div>Loading trip members...</div>;
  }

  if (loadingDelete) {
    return <div>Deleting trip member...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
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
       <h2>Edit Trip Members</h2>

       <form onSubmit={handleSubmit} class="trip-day-form">
        <div>
          <label><strong>Current Trip Members:</strong></label>
        <ol>
          {tripMembers.map((user) => (
            <li key={user.user_id}>{user.username} <button onClick={() => deleteTripMember(user.user_id, user.username, tripId)} style={{
              fontSize: '17px',
              backgroundColor: 'transparent',
              border: 'none',
              cursor: loading ? 'not-allowed' : 'pointer',
              padding: '10px',
              color: loading ? '#999' : '#1E90FF',}}>
            <FontAwesomeIcon icon={faTimes} style={{ marginRight: '8px' }} />
            </button></li>
            ))}
        </ol>

        </div>

        <div>
        <label>Add Existing Users to Trip:</label>
          <input
          type="text"
            value={newMember}
            placeholder={'Enter username'}
            onChange={handleNewMemberChange}
          />
        </div>

        <button type="submit">Submit</button>
       </form>
    </div>
  )
};


export default EditTripMembers;