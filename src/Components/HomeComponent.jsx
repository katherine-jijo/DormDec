import React, { useState } from "react";
import DormDecidersLogo from "../assets/dormLogo.png";
import ConfirmationButton from "./ConfirmationButton";
import JoinBlockForm from "./JoinBlockForm"; // Import the JoinBlockForm component
import CreateBlockForm from "./CreateBlockForm"; // Import the CreateBlockForm component
import LeaveBlockForm from "./LeaveBlockForm"; // Import the LeaveBlockForm component
import joinBlock from "./joinBlock"; // Import the joinBlock function
import createBlock from "./createBlock"; // Import the createBlock function
import leaveBlock from "./leaveBlock"; // Import the leaveBlock function
import StudentSearchButton from "./StudentSearchButton"; // Import the StudentSearchButton component
import { db } from '../firebaseConfig.js'; // Import your Firebase database reference
import { ref, get } from "firebase/database";
import "../Sass/HomeComponent.scss";

const Home = () => {
    const [showConfirmationOptions, setShowConfirmationOptions] = useState(false);
    const [matchingResults, setMatchingResults] = useState([]);
    //for see room button
    const [showInput, setShowInput] = useState(false);
    const [UserhofstraID, setUserhofstraID] = useState("");
    const [roomAssignment, setRoomAssignment] = useState('');
    const handleChange = (event) => {
        setUserhofstraID(event.target.value);
    };

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

    //backend api
    const handleDueDateMatching = () => {
        fetch("http://127.0.0.1:5000/dueDateMatching")
            .then((response) => response.json())
            .then((data) => {
                console.log(data); // Output the data received from the Flask server
                setMatchingResults(data); // Update the matchingResults state with the data received from the server
            })
            .catch((error) => {
                console.error("Error:", error);
                // Handle any errors that occur during the request
            });
    };

    const handleEnterID = () => {
        setShowInput(true);
    };

    const handleClick = async () => {
        // Your logic here to handle the user input
        console.log("User Hofstra ID:", UserhofstraID);

        // Reset the input field and hide the input box (idk if need thse lines)
        //setUserhofstraID('');
        //setShowInput(false);

        // Make a Firebase call to fetch the user's data here i think???
        var userID = (await get(ref(db, 'localIdStorage/' + UserhofstraID.toString()))).val();
        var roomNum = (await get(ref(db, 'users/' + userID + '/roomAssignment'))).val();
        setRoomAssignment('Room assignment is: ' + roomNum);

    };
    return (
        <div className="home-wrapper">
            <div className="logo-container">
                <img src={DormDecidersLogo} alt="Dorm Deciders Logo" className="logo" />
            </div>
            <div className="content-wrapper">
                <div className="slogan">
                    <h1>Enhance your dormitory experience</h1>
                    <p>
                        Elevate your dorm life with Dorm Deciders. From questionnaire to match to confirmation, we've
                        got you covered. Start your journey now!
                    </p>
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
                    <button className="rounded-rect-btn" onClick={handleDueDateMatching}>
                        Due Date Matching
                    </button>
                    <div className="see-room">
                        {!showInput && (
                            <button className="rounded-rect-btn" onClick={handleEnterID}>
                                See Living Arrangement
                            </button>
                        )}
                        {showInput && (
                            //takes hof id
                            <>
                                <div>
                                    <button className="rounded-rect-btn" onClick={handleClick}>
                                        See Living Arrangement
                                    </button>
                                </div>
                                <div>
                                    <div className="input-box">
                                        <input
                                            type="text"
                                            value={UserhofstraID}
                                            onChange={handleChange}
                                            placeholder="Enter Hofstra ID"
                                        />
                                    </div>
                                </div>
                            </>
                        )}
                        {roomAssignment && (
                            <div>
                                <h2>Room information:</h2>
                                <ul>{roomAssignment}</ul>
                            </div>
                        )}
                    </div>
                    
                </div>
            </div>
        </div>
    );
};
const QuestionnaireButton = () => {
    const openGoogleForm = () => {
        window.open(
            "https://docs.google.com/forms/d/e/1FAIpQLScgA-inXShLiwMvLYxTeNf1j24HoeIeJkrNPn1LfcR2OlKndg/viewform?usp=sf_link",
            "_blank"
        );
    };

    return (
        <button className="rounded-rect-btn" onClick={openGoogleForm}>
            Questionnaire
        </button>
    );
};

export default Home;
