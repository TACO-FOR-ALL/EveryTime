import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { doc, getDoc, updateDoc } from 'firebase/firestore';
import { db } from './firebase';
import './css/RegisterForm.css'; 

function ChangeProfile() {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [school, setSchool] = useState('');
  const [classnum, setClassnum] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      if (currentUser) {
        const userDoc = doc(db, 'users', currentUser.uid);
        const docSnapshot = await getDoc(userDoc);
        if (docSnapshot.exists()) {
          const userData = docSnapshot.data();
          setName(userData.name);
          setSchool(userData.school);
          setClassnum(userData.classnum);
        }
      }
    };
    fetchUserData();
  }, [currentUser]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const userDoc = doc(db, 'users', currentUser.uid);
      await updateDoc(userDoc, {
        name,
        school,
        classnum
      });
      navigate('/ProfilePage'); // Redirect to profile page after successful update
    } catch (error) {
      setError('Failed to update profile. Please try again.');
    }
  };

  return (
    <div className="register-container">
      <div className="title-container">
        <h1 className="title">GPA</h1>
        <p className="subtitle">Management Platform</p>
      </div>
      <form onSubmit={handleSubmit} className="register-form">
        <input
          type="name"
          className="register-input"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="text"
          className="register-input"
          placeholder="School"
          value={school}
          onChange={(e) => setSchool(e.target.value)}
          required
        />
        <input
          type="text"
          className="register-input"
          placeholder="Year (grade: 1,2,3,4)"
          value={classnum}
          onChange={(e) => setClassnum(e.target.value)}
          required
        />
        <button type="submit" className="register-button">Update</button>
        {error && <div className="error-message">{error}</div>}
      </form>
      <div className="footer-links">
      </div>
    </div>
  );
}

export default ChangeProfile;