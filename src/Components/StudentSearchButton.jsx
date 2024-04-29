import { getTopUserList, getUserInfo } from './StudentSearch'; // Correct file path and extension
import { useState } from 'react';

const StudentSearchButton = () => {
    const [userInfo, setUserInfo] = useState([]);

    const handleClick = async () => {
        try {
            const topUserList = await getTopUserList('userHofstraID');
            const users = await getUserInfo(topUserList);
            setUserInfo(users);
        } catch (error) {
            console.error('Error getting user info:', error);
        }
    };

    return (
        <div className="student-search">
            <button className="rounded-rect-btn" onClick={handleClick}>
                Student Search
            </button>
            {userInfo && (
                <div className="dropdown">
                    <h2>User Information:</h2>
                    <ul>
                        {userInfo.map((user, index) => (
                            <li key={index}>
                                Name: {user.name}, User email: {user.userEmail}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );

};

export default StudentSearchButton;