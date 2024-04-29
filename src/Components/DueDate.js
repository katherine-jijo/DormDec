import React from 'react';

const YourComponent = () => {
    const handleDueDateMatching = async () => {
        try {
            const response = await fetch('http://localhost:5000/due_date_matching');
            if (response.ok) {
                const data = await response.json();
                console.log(data);
            } else {
                console.error('Failed to perform due date matching:', response.status);
            }
        } catch (error) {
            console.error('Error during due date matching:', error);
        }
    };

    return (
        <div>
            <button onClick={handleDueDateMatching}>Perform Due Date Matching</button>
        </div>
    );
};

export default YourComponent;
