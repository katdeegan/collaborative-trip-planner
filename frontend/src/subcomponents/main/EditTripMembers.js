// FormPage.js (The form where you select multiple options)
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate  } from 'react-router-dom';
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
};


export default EditTripMembers;