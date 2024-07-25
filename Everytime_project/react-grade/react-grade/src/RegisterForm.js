import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './css/RegisterForm.css'; 
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { doc, setDoc } from 'firebase/firestore';
import { auth, db } from './firebase';

function RegisterForm({ onLogin }) {
  const [pw, setPw] = useState('');
  const [pwConfirm, setPwConfirm] = useState('');
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [school, setSchool] = useState('');
  const [classnum, setClassnum] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (pw !== pwConfirm) {
      setError('Please double-check your password');
      return;
    }
    if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@]{8,}$/.test(pw)) {
      setError('You have to keep password form (English + Number, Special characters: !,@)');
      return;
    }

    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, pw);
      const user = userCredential.user;

      await setDoc(doc(db, 'users', user.uid), {
        email,
        name,
        school,
        classnum,
      });

      onLogin(user);
      navigate('/mainhome');
    } catch (error) {
      setError('Failed to register. Please try again.');
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
          type="email"
          className="register-input"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          className="register-input"
          placeholder="Password"
          value={pw}
          onChange={(e) => setPw(e.target.value)}
          required
        />
        <input
          type="password"
          className="register-input"
          placeholder="Confirm Password"
          value={pwConfirm}
          onChange={(e) => setPwConfirm(e.target.value)}
          required
        />
        <input
          type="text"
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
        <button type="submit" className="register-button">Join us</button>
        {error && <div className="error-message">{error}</div>}
      </form>
      <div className="footer-links">
      </div>
    </div>
  );
}

export default RegisterForm;
