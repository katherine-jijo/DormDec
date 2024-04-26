import React from 'react';
import DormDecidersLogo from '../assets/dormLogo.png';
import '../Sass/HomeComponent.scss';

const Home = () => {
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
          <StudentSearchButton />
        <button className="rounded-rect-btn">Confirmation</button>      
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


const StudentSearchButton = () => {
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
  
export default Home;
