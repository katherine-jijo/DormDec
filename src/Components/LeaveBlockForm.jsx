//this file just renders button the button 


import React, { useState } from 'react';

const LeaveBlockForm = ({ onLeave }) => {
  const [showForm, setShowForm] = useState(false);
  const [userID, setUserID] = useState('');

  const handleLeave = () => {
    setShowForm(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onLeave(userID);
    setShowForm(false);
    setUserID('');
  };

  return (
    <div>
      {!showForm && (
        <button onClick={handleLeave}>Leave Block</button>
      )}
      {showForm && (
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter user ID"
            value={userID}
            onChange={(e) => setUserID(e.target.value)}
          />
          <button type="submit">Submit</button>
        </form>
      )}
    </div>
  );
};

export default LeaveBlockForm;
