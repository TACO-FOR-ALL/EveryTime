import React from 'react';
import { useNavigate } from 'react-router-dom';
import './css/ProfilePage.css';

function ContactAdmin() {
   
    const navigate = useNavigate();

    return (
        <div className="profile-container">
            <div className="profile-section">
             <div>
              <h2 className="section-header">Contact Admin</h2>
              <p className="center-text">Contact the administrator's contact information below.</p>
              <p className="center-text">Email: sunlift10000@gmail.com</p>
              <button className="small-button" onClick={() => navigate('/ProfilePage')}>Back</button>
             </div>
            </div>
        </div>
    );
}

export default ContactAdmin;