import React, { useState } from "react";
import { RegisterAPI } from "../api/AuthAPI";
import "../Sass/RegisterComponent.scss";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import DormDecidersLogo from "../assets/dormLogo.png";

export default function RegisterComponent() {
    let navigate = useNavigate();
    const [credentials, setCredentials] = useState({ email: "", password: "", studentID: "" });

    const register = async () => {
        try {
            let res = await RegisterAPI(credentials.email, credentials.password, credentials.studentID);
            if (res.user){
                toast.success("Registered Successfully!");
                localStorage.setItem("userEmail", res.user.email);
                navigate("/home");
            }
            else throw err;
        } catch (err) {
            console.log(err);
            toast.error("Registration Failed. Please try again.");
        }
    };

    return (
        <div className="register-wrapper">
            <div className="register-wrapper-inner">
                <img src={DormDecidersLogo} className="dormLogo" />

                <div className="register-wrapper-inner">
                    <h1 className="heading">Register</h1>
                    <p className="sub-heading">Create your Dorm Deciders Account</p>

                    <div className="auth-inputs">
                        <input
                            onChange={(event) => setCredentials({ ...credentials, email: event.target.value })}
                            type="email"
                            className="common-input"
                            placeholder="Email Address"
                        />
                        <input
                            onChange={(event) => setCredentials({ ...credentials, password: event.target.value })}
                            type="password"
                            className="common-input"
                            placeholder="Password"
                        />
                        <input
                            onChange={(event) => setCredentials({ ...credentials, studentID: event.target.value })}
                            type="text"
                            className="common-input"
                            placeholder="Hofstra Student ID"
                        />
                    </div>
                    <button onClick={register} className="register-btn">
                        Register
                    </button>
                </div>
                <hr className="hr-text" data-content="or" />
                <div className="google-btn-container">
                    <p className="go-to-login">
                        Already have an account?{" "}
                        <span className="join-now" onClick={() => navigate("/")}>
                            Login now
                        </span>
                    </p>
                </div>
            </div>
        </div>
    );
}
