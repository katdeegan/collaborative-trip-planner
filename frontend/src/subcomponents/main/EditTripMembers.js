// FormPage.js (The form where you select multiple options)
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate  } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';  
import { faTimes  } from '@fortawesome/free-solid-svg-icons'; 
import '../styles/add-users-form.css'

const EditTripMembers = () => {
  // TODO - pass this info in from previous page
  const tripMemberData = [{username: "kat"}, {username: "sierra"}]

  const [newMember, setNewMember] = useState();
  const handleNewMemberChange = (event) => setNewMember(event.target.value);

  const handleSubmit = (event) => {
    event.preventDefault();
  };

  const deleteTripMember = async () => { 
    console.log("Deleting trip member...")
    const userConfirmed = window.confirm(`Are you sure you want to delete this user from the trip?`);
    if (userConfirmed) {
      // Proceed with the action if user clicks OK
      console.log("Action confirmed!");
      // You can execute any action here, such as calling an API or executing a function
    } else {
      // Action is canceled if user clicks Cancel
      console.log("Action canceled.");
    }

  };

  return (
    <div className="form-container">
       <h2>Edit Trip Members</h2>

       <form onSubmit={handleSubmit} class="trip-day-form">
        <div>
          <label><strong>Current Trip Members:</strong></label>
        <ol>
          {tripMemberData.map((user, index) => (
            <li key={index}>{user.username} <button onClick={deleteTripMember}>
            <FontAwesomeIcon icon={faTimes} style={{ marginRight: '8px' }} />
            </button></li>
            ))}
        </ol>

        </div>

        <div>
        <label>Add Existing Users to Trip:</label>
          <textarea
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