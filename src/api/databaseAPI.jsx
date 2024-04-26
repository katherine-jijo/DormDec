// databaseAPI.jsx
import { set, ref } from "firebase/database";
import { db } from "../firebaseConfig";

// Function to save user data to the database
export const saveUserData = async (localId, email, studentID) => {
  const userData = {
    localId: localId,
    email: email,
    studentID: studentID
  };

  // Save userData under the user's localId in your database
  await set(ref(db, 'users/' + localId), userData);
};
