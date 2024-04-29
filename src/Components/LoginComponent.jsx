import React, { useState } from "react";
import { LoginAPI } from "../api/AuthAPI";
import "../Sass/LoginComponent.scss";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import DormDecidersLogo from "../assets/dormLogo.png";

export default function LoginComponent() {
    let navigate = useNavigate();
    const [credentials, setCredentials] = useState({ email: "", password: "", studentID: "" });

    const login = async () => {
        try {
            let res = await LoginAPI(credentials.email, credentials.password, credentials.studentID);
            toast.success("Signed In to Dorm Deciders!");
            localStorage.setItem("userEmail", res.user.email);
            navigate("/home");
        } catch (err) {
            console.log(err);
            toast.error("Please Check your Credentials");
        }
    };

    return (
        <div className="login-wrapper">
            <div className="login-wrapper-inner">
                <img src={DormDecidersLogo} className="dormLogo" />

                <div className="login-wrapper-inner">
                    <h1 className="heading">Sign in</h1>
                    <p className="sub-heading">Find your Perfect Match!</p>

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
                    <button onClick={login} className="login-btn">
                        Sign in
                    </button>
                </div>
                <hr className="hr-text" data-content="or" />
                <div className="google-btn-container">
                    <p className="go-to-signup">
                        New to Dorm Deciders?{" "}
                        <span className="join-now" onClick={() => navigate("/register")}>
                            Join now
                        </span>
                    </p>
                </div>
            </div>
        </div>
    );
}
