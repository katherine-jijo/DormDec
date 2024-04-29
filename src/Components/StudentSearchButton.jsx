import React, { useState, useEffect } from 'react';
import { db } from '../firebaseConfig.js';
import { getTopUserList, getUserInfo } from './StudentSearch'; 

const StudentSearchButton = () => {
    const [userInfo, setUserInfo] = useState([]);
    const [showInput, setShowInput] = useState(false);
    const [UserhofstraID, setHofstraID] = useState('');

    const handleClick = async () => {
        try {
            const topUserList = await getTopUserList(UserhofstraID);
            const users = await getUserInfo(topUserList);
            setUserInfo(users);
            setShowInput(false); // Hide input box after getting user info
        } catch (error) {
            console.error('Error getting user info:', error);
        }
    };

    const handleEnterID = () => {
        setShowInput(true);
    };

    const handleChange = (e) => {
        setHofstraID(e.target.value);
    };

    return (
        <div className="student-search">
            {!showInput && (
                <button className="rounded-rect-btn" onClick={handleEnterID}>
Student Search                </button>
            )}
            {showInput && (
                <div className="input-box">
                    <input type="text" value={UserhofstraID} onChange={handleChange} placeholder="Enter Hofstra ID" />
                    <button className="rounded-rect-btn" onClick={handleClick}>
                        Confirm
                    </button>
                </div>
            )}
            {userInfo && (
                <div className="dropdown">
                    <h2>User Information:</h2>
                    <ul>
                        {userInfo.map((user, index) => (
                            <li key={index}>
                                Name: {user.name}, User email: {user.email}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default StudentSearchButton;