import React, { useState, useEffect } from 'react';
import '../styles/form-styles.css'; 

const ChangeTripDatesModal = ({ isOpen, onClose, startDate, endDate, onSave }) => {
  const [newStartDate, setNewStartDate] = useState(startDate);
  const [newEndDate, setNewEndDate] = useState(endDate);

  // Update dates when the modal is reopened with new values
  useEffect(() => {
    setNewStartDate(startDate);
    setNewEndDate(endDate);
  }, [startDate, endDate]);

  if (!isOpen) return null;

  const handleSave = () => {
    // Pass back the new dates to the parent component
    onSave(newStartDate, newEndDate);
    onClose(); // Close the modal after saving
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>X</button>
        <h2>Edit Trip Dates</h2>
        <div className="modal-form">
          <label htmlFor="start-date">Start Date:</label>
          <input
            type="date"
            id="start-date"
            value={newStartDate}
            onChange={(e) => setNewStartDate(e.target.value)}
          />
          <label htmlFor="end-date">End Date:</label>
          <input
            type="date"
            id="end-date"
            value={newEndDate}
            onChange={(e) => setNewEndDate(e.target.value)}
          />
        </div>
        <button className="save-btn" onClick={handleSave}>Save</button>
      </div>
    </div>
  );
};

export default ChangeTripDatesModal;
