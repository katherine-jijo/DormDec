// ConfirmationButton.jsx

import React from 'react';
import { db } from '../firebaseConfig';


//confirm button logic here? 


const ConfirmationButton = ({ onConfirmation }) => {
  const handleConfirmation = () => {
    onConfirmation();
  };

  return (
    <div>
      <button className="rounded-rect-btn" onClick={handleConfirmation}>
        Confirmation
      </button>
    </div>
  );
};

export default ConfirmationButton;
