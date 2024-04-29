import React, { useState } from 'react';
import DormDecidersLogo from '../assets/dormLogo.png';
import ConfirmationButton from './ConfirmationButton';
import JoinBlockForm from './JoinBlockForm'; // Import the JoinBlockForm component
import CreateBlockForm from './CreateBlockForm'; // Import the CreateBlockForm component
import LeaveBlockForm from './LeaveBlockForm'; // Import the LeaveBlockForm component
import joinBlock from './joinBlock'; // Import the joinBlock function
import createBlock from './createBlock'; // Import the createBlock function
import leaveBlock from './leaveBlock'; // Import the leaveBlock function
import StudentSearchButton from './StudentSearchButton'; // Import the StudentSearchButton component

import '../Sass/HomeComponent.scss';

const Home = () => {
  const [showConfirmationOptions, setShowConfirmationOptions] = useState(false);

  const handleConfirmation = () => {
    setShowConfirmationOptions(true);
  };

  const handleJoin = (userID, leaderID) => {
    // Call the joinBlock function with the provided user and leader IDs
    joinBlock(userID, leaderID);
    // Additional logic if needed
  };

  const handleCreate = (userID) => {
    // Call the createBlock function with the provided user ID
    createBlock(userID);
    // Additional logic if needed
  };

  const handleLeave = (userID) => {
    leaveBlock(userID);
    // Additional logic if needed
  };

  return (
    <div className="home-wrapper">
      <div className="logo-container">
        <img src={DormDecidersLogo} alt="Dorm Deciders Logo" className="logo" />
      </div>
      <div className="content-wrapper">
        <div className="slogan">
          <h1>Enhance your dormitory experience</h1>
          <p>Elevate your dorm life with Dorm Deciders. From questionnaire to match to confirmation, we've got you covered. Start your journey now!</p>
        </div>
        <div className="buttons">
          <QuestionnaireButton />
          <StudentSearchButton /> {/* Include the StudentSearchButton component here */}
          <ConfirmationButton onConfirmation={handleConfirmation} />
          {showConfirmationOptions && (
            <>
              <JoinBlockForm onJoin={joinBlock} />
              <CreateBlockForm onCreate={createBlock} />
              <LeaveBlockForm onLeave={leaveBlock} />
            </>
          )}
        </div>
      </div>
    </div>
  );
};

const QuestionnaireButton = () => {
    const openGoogleForm = () => {
      window.open('https://docs.google.com/forms/d/e/1FAIpQLScgA-inXShLiwMvLYxTeNf1j24HoeIeJkrNPn1LfcR2OlKndg/viewform?usp=sf_link', '_blank');
    };
  
    return (
      <button className="rounded-rect-btn" onClick={openGoogleForm}>
        Questionnaire
      </button>
    );
};

export default Home;
