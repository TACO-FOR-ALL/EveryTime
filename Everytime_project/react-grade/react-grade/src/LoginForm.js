import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './css/LoginForm.css';
import { signInWithEmailAndPassword, signInWithPopup } from 'firebase/auth';
import { auth, googleProvider, db } from './firebase';
import { doc, setDoc, getDoc, collection, getDocs } from 'firebase/firestore';

function LoginForm({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const initializeUserData = async (userId, email, displayName) => {
    const userDoc = doc(db, 'users', userId);
    const userSnap = await getDoc(userDoc);

    if (!userSnap.exists()) {
      await setDoc(userDoc, {
        email,
        name: displayName || '',
        school: '',
        classnum: ''
      });

      const departments = ['Computer Science', 'Economics and Trade'];
      const semesters = ['2021-2022-1', '2021-2022-2', '2021-2022-3', '2022-2023-1', '2022-2023-2', '2022-2023-3', '2023-2024-1', '2023-2024-2', '2023-2024-3', '2024-2025-1', '2024-2025-2'];

      for (const department of departments) {
        for (const semester of semesters) {
          const coursesRef = collection(db, `courses/${department}/${semester}/courses`);
          const coursesSnap = await getDocs(coursesRef);
          for (const course of coursesSnap.docs) {
            const courseData = course.data();
            const userCourseRef = doc(db, `users/${userId}/departments/${department}/${semester}/courses/${course.id}`);
            await setDoc(userCourseRef, {
              courseName: courseData.courseName,
              credits: courseData.credits,
              score: 'N/A'
            });
          }
        }
      }
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      await initializeUserData(user.uid, user.email, user.displayName);
      onLogin(user);
      navigate('/mainhome');
    } catch (error) {
      setError('Failed to log in. Please check your email and password.');
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const user = result.user;
      await initializeUserData(user.uid, user.email, user.displayName);
      onLogin(user);
      navigate('/mainhome');
    } catch (error) {
      setError('Failed to log in with Google.');
    }
  };

  return (
    <div className="login-container">
      <div className="title-container">
        <h1 className="title">GPA</h1>
        <p className="subtitle">Management Platform</p>
      </div>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="email"
          className="login-input"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          className="login-input"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" className="login-button">Login</button>
        {error && <div className="error-message">{error}</div>}
        <button onClick={handleGoogleLogin} className="google-login-button">
          <img src="https://developers.google.com/identity/images/btn_google_signin_dark_normal_web.png" alt="Google sign-in" />
        </button>
      </form>
      <div className="links-container">
        <Link to="/RegisterForm" className="auth-link">Join Us</Link>
        <Link to="/PasswordResetPage" className="auth-link">Find Password</Link>
      </div>
      <div className="footer">
        <span className="footer-text">
          By clicking continue, you agree to our Terms of Service and Privacy Policy
        </span>
      </div>
    </div>
  );
}

export default LoginForm;
