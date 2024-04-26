//(Component file)
//this file just renders button the button 


import React, { useState } from 'react';

const JoinBlockForm = ({ onJoin }) => {
  const [showForm, setShowForm] = useState(false);
  const [userID, setUserID] = useState('');
  const [leaderID, setLeaderID] = useState('');

  const handleJoin = () => {
    setShowForm(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onJoin(userID, leaderID);
    setShowForm(false);
    setUserID('');
    setLeaderID('');
  };

  return (
    <div>
      {!showForm && (
        <button onClick={handleJoin}>Join Block</button>
      )}
      {showForm && (
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter user ID"
            value={userID}
            onChange={(e) => setUserID(e.target.value)}
          />
          <input
            type="text"
            placeholder="Enter leader ID"
            value={leaderID}
            onChange={(e) => setLeaderID(e.target.value)}
          />
          <button type="submit">Submit</button>
        </form>
      )}
    </div>
  );
};

export default JoinBlockForm;
