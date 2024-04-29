import React from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider } from "react-router-dom";
import { router } from './Routes';
import { app, auth } from "./firebaseConfig";
import './index.css'
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

//import { app } from "./firebaseConfig";

// Assuming you have a way to get the user's Hofstra ID
//const user = auth.currentUser;
//const userHofstraId = user ? user.hofstraId : null;

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
      <RouterProvider router={router} />
      <ToastContainer />
  </React.StrictMode>,
)
