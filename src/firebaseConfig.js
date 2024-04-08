// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";


// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries


const firebaseConfig = {
  apiKey: "AIzaSyBZ_Nnybektn1URt1xv-A6_FTnLJs1adzQ",
  authDomain: "dorm-deciders.firebaseapp.com",
  databaseURL: "https://dorm-deciders-default-rtdb.firebaseio.com",
  projectId: "dorm-deciders",
  storageBucket: "dorm-deciders.appspot.com",
  messagingSenderId: "908311322524",
  appId: "1:908311322524:web:8d53c41f9b42667a8fb259",
  measurementId: "G-V8BYWBGHE6"
};



// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
export { auth, app };

