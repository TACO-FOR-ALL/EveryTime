import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAuth, reauthenticateWithCredential, EmailAuthProvider, updatePassword } from 'firebase/auth';
import './css/LoginForm.css';

function PasswordChange() {
    const navigate = useNavigate();
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmNewPassword, setConfirmNewPassword] = useState('');
    const [error, setError] = useState('');
    const [isGoogleUser, setIsGoogleUser] = useState(false);
    const auth = getAuth();

    useEffect(() => {
        const user = auth.currentUser;
        if (user && user.providerData.some(provider => provider.providerId === 'google.com')) {
            setIsGoogleUser(true);
        }
    }, [auth.currentUser]);

    const handleChangePassword = async (event) => {
        event.preventDefault();

        if (newPassword !== confirmNewPassword) {
            setError('New password does not match');
            return;
        }

        if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@]{8,}$/.test(newPassword)) {
            setError('Password must be at least 8 characters long and include letters, numbers, and special characters (!, @)');
            return;
        }

        try {
            const user = auth.currentUser;
            const credential = EmailAuthProvider.credential(user.email, currentPassword);
            await reauthenticateWithCredential(user, credential);

            await updatePassword(user, newPassword);
            alert('Your password has been successfully changed');
            navigate('/login');
        } catch (error) {
            setError('Failed to change password. Please check your current password and try again.');
        }
    };

    return (
        <div className="login-container">
            <div className="title-container">
                <h1 className="title">Change Password</h1>
                <p>You have to keep password form (English + Number, Special characters: !,@)</p>
            </div>
            {isGoogleUser ? (
                <div className="login-form">
                    <p className="error-message">Google login user do not need to change password</p>
                    <button onClick={() => navigate('/profilePage')} className="login-button">Back to Profile</button>
                </div>
            ) : (
                <form onSubmit={handleChangePassword} className="login-form">
                    <input
                        type="password"
                        className="login-input"
                        placeholder="Current password"
                        value={currentPassword}
                        onChange={(e) => setCurrentPassword(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        className="login-input"
                        placeholder="New password"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        className="login-input"
                        placeholder="Confirm new password"
                        value={confirmNewPassword}
                        onChange={(e) => setConfirmNewPassword(e.target.value)}
                        required
                    />
                    {error && <div className="footer-text">{error}</div>}
                    <button type="submit" className="login-button">Change Password</button>
                </form>
            )}
        </div>
    );
}

export default PasswordChange;