import React, { useState, useEffect } from 'react';
import { db } from '../firebaseConfig.js'; // Import your Firebase database reference
//import * as firebase from 'f../firebaseConfig.js';

import 'firebase/auth';
import 'firebase/database';





 const StudentSearchButton = () => {
    const [preferences, setPreferences] = useState(null);

    const createPreferenceLists = async () => {
        const response = await fetch('/runPreferenceLists', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // Add body data if needed
        });
        if (response.ok) {
            console.log('Preference lists created successfully');
        } else {
            console.error('Failed to create preference lists');
        }
    };

    const getUserPreferences = async () => {
        const user = firebase.auth().currentUser;
        if (user) {
            const userHofstraID = user.uid; // Use the user's UID as the Hofstra ID
            try {
                const snapshot = await firebase.database().ref(`preferenceLists/${userHofstraID}/topUserList`).get();
                if (snapshot.exists()) {
                    // Convert object to array
                    const data = snapshot.val();
                    const preferencesArray = Object.values(data);
                    setPreferences(preferencesArray);
                } else {
                    console.error('No data available');
                }
            } catch (error) {
                console.error('Error getting preference list:', error);
            }
        } else {
            console.error('No user logged in');
        }
    };
    

    useEffect(() => {
        getUserPreferences();
    }, []);

    return (
      <div>
          <button className="rounded-rect-btn" onClick={createPreferenceLists}>
              Student Search
          </button>
          {preferences && (
              <div>
                  <h2>Preference List:</h2>
                  <ul>
                      {preferences.map((preference, index) => (
                          <li key={index}>{preference}</li>
                      ))}
                  </ul>
              </div>
          )}
      </div>
  );
};
export default StudentSearchButton;
