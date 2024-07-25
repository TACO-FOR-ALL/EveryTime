import React from 'react';
import { useNavigate } from 'react-router-dom';
import './css/NavigationBar.css';

const NavigationBar = () => {
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="bottom-nav">
      <ul>
        <li><button onClick={() => handleNavigate('/MainHome')} className="nav-button">Home</button></li>
        <li><button onClick={() => handleNavigate('/CurrentGPA')} className="nav-button">Edit Score</button></li>
        <li><button onClick={() => handleNavigate('/EstimatedGPA')} className="nav-button">Estimated GPA</button></li>
        <li><button onClick={() => handleNavigate('/ProfilePage')} className="nav-button">Profile</button></li>
      </ul>
    </div>
  );
};

export default NavigationBar;
