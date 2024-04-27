// CreateBlockForm.jsx
//this file just renders button the button 

import React, { useState } from 'react';

const CreateBlockForm = ({ onCreate }) => {
  const [showForm, setShowForm] = useState(false);
  const [userID, setUserID] = useState('');

  const handleCreate = () => {
    setShowForm(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onCreate(userID);
    setShowForm(false);
    setUserID('');
  };

  return (
    <div>
      {!showForm && (
        <button onClick={handleCreate}>Create Block</button>
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

export default CreateBlockForm;
