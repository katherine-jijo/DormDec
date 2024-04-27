import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup,
  signOut
} from "firebase/auth";
import { auth } from "../firebaseConfig";
import { saveUserData } from "./databaseAPI";


// Define the RegisterAPI function
export const RegisterAPI = async (email, password, studentID) => {
  try {
    let response = await createUserWithEmailAndPassword(auth, email, password);
    if (response.user) {
      // Save user data to the database
      await saveUserData(response.user.uid, email, studentID);
    }
    return response;
  } catch (err) {
    return err;
  }
};


export const LoginAPI = async (email, password, studentID) => {
    try {
        const response = await signInWithEmailAndPassword(auth, email, password);
        if (response.user) {
            // You can save it to the user object if needed
            response.user.studentID = studentID;
        }
        return response;
    } catch (err) {
      return err;
    
  };
  
  /* old reg 
  
  export const RegisterAPI = (email, password) => {
      try {
        let response = createUserWithEmailAndPassword(auth, email, password);
        return response;
      } catch (err) {
        return err;
      }
    };
  */
  
    // RegisterAPI function
  }
