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
          <button>Questionnaire</button>
          <button>Student Search</button>
          <button>Confirmation</button>
        </div>
      </div>
    </div>
  );
};

export default Home;
