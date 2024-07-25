import React, { useState } from 'react';
import { sendPasswordResetEmail, fetchSignInMethodsForEmail } from 'firebase/auth';
import './css/PasswordResetPage.css';
import { auth } from './firebase';
import { useNavigate } from 'react-router-dom';

function PasswordResetPage() {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handlePasswordReset = async () => {
        try {
            const signInMethods = await fetchSignInMethodsForEmail(auth, email);
            if (signInMethods.includes('google.com')) {
                setError('This email is associated with a Google account. Password reset is not available.');
                return;
            }

            await sendPasswordResetEmail(auth, email);
            setMessage('A password reset email has been sent to your email address.');
            setError('');
            setTimeout(() => {
                navigate('/login');
            }, 1000); // 1초 후 로그인 페이지로 이동
        } catch (error) {
            setError('Failed to send password reset email. Please check your email and try again.');
            setMessage('');
        }
    };

    return (
        <div className="password-reset-container">
            <div className="title-container">
                <h1>GPA</h1>
                <p>Management Platform</p>
            </div>
            <div className="content">
                <h3>You can initialize your password through the email you entered when you signed up.</h3>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email you entered when you signed up"
                    className="email-input"
                />
                <button onClick={handlePasswordReset} className="reset-button">Find Password and Go to Login</button>
                {message && <div className="message">{message}</div>}
                {error && <div className="error-message">{error}</div>}
            </div>
            <div className="footer">
                <span className="footer-text">※If you haven't received an email, please check your spam mailbox.</span>
            </div>
            <span className="footer-text">※If you have a registered ID, we will inform you of the password through the email you entered.</span>
        </div>
    );
}

export default PasswordResetPage;
