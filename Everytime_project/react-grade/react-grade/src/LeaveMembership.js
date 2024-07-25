import React from 'react';
import { useNavigate } from 'react-router-dom';
import './css/ProfilePage.css';

function LeaveMembership() {
    const navigate = useNavigate();

    const handleLeaveMembership = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_HOST}/users/LeaveMembership`, {
                method: 'DELETE',
            });

            const data = await response.json();

            if (response.ok) {
                alert('Membership withdrawal completed');
                navigate('/login'); 
            } else {
                alert(data.message || 'Failed to Membership Withdrawal');
            }
        } catch (error) {
            alert('An error occurred while processing membership withdrawal');
            console.error('Leave membership error:', error);
        }
    };

    return (
        <div className="profile-container">
            <div className="profile-section">
             <div>
              <h2 className="section-header">Membership Withdrawal</h2>
              <p className="center-text">Really want Membership Withdrawal?</p>
              <button className="small-button" onClick={handleLeaveMembership}>Membership Withdrawal</button>    
             </div>
            </div>
        </div>
    );
}

export default LeaveMembership;