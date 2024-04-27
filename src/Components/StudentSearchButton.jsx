
import React from 'react';

//student search button logic 



export const StudentSearchButton = () => {
    const searchStudents = async () => {
      // Perform the search logic here
      // You can use the Firebase database reference and query for the closest matches
      // For simplicity, let's assume a function `performSearch` that returns the search results
      const searchResults = await performSearch();
      
      // Display the search results (e.g., alert, modal, etc.)
      alert(JSON.stringify(searchResults));
    };
  
    return (
      <button className="rounded-rect-btn" onClick={searchStudents}>
        Student Search
      </button>
    );
  };
