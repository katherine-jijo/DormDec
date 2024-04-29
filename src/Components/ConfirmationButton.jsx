// ConfirmationButton.jsx

import React from 'react';
import { db } from '../firebaseConfig';


//confirm button logic here? 


const ConfirmationButton = ({ onConfirmation }) => {
  const handleConfirmation = () => {
    onConfirmation();
  };

  return (
      <button className="rounded-rect-btn" onClick={handleConfirmation}>
        Confirmation
      </button>
  );
};

export default ConfirmationButton;
