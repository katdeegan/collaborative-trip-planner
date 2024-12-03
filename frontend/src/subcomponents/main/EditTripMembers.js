// FormPage.js (The form where you select multiple options)
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate  } from 'react-router-dom';
<<<<<<< HEAD
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
=======
import '../styles/add-users-form.css'

const EditTripMembers = () => {
    // TODO - page should be form with text field. can add multiple users as comma-seperated list of usernames.
    // if username(s) not found in database, should get error messgage - "One or more user accounts not found."
    const navigate = useNavigate(); 
  const [selectedValues, setSelectedValues] = useState([]); // For holding selected values
  const [dropdownData, setDropdownData] = useState([]); // For holding dropdown options data

  const { tripId } = useParams();

  // Fetch the data for dropdown (replace with actual API call)
  useEffect(() => {
    // Simulating an API call to get data
    const fetchData = async () => {
      const data = [
        { id: 1, username: 'user1' },
        { id: 2, username: 'user2' },
        { id: 3, username: 'user3' },
        { id: 4, username: 'user4' },
      ];
      setDropdownData(data);
    };

    fetchData();
  }, []);

  // Handle selection changes
  const handleChange = (event) => {
    const options = Array.from(event.target.selectedOptions, (option) => option.value);
    setSelectedValues(options);
  };

  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    // Redirect to another page after submission
    console.log('Selected values:', selectedValues);
    navigate(`/trip/${tripId}`)
  };

  return (
    <div>
      <h1>Select Options</h1>
      <form className="add-users-form" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="select-multiple">Choose options:</label>
          <select className="users-select"
            id="select-multiple"
            multiple
            value={selectedValues}
            onChange={handleChange}
          >
            {dropdownData.map((option) => (
              <option key={option.id} value={option.value}>
                {option.value}
              </option>
            ))}
          </select>
        </div>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
>>>>>>> ebef2826be125fdbb04d886d282e4173a796357a
};


export default EditTripMembers;