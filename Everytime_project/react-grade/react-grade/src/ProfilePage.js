import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { doc, getDoc } from 'firebase/firestore';
import { db } from './firebase';
import NavigationBar from './NavigationBar';
import './css/ProfilePage.css';
import './css/MainHome.css';

function ProfilePage() {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();

  const [profileImg, setProfileImg] = useState('/BKD.jpg'); // 기본 이미지 경로
  const [error, setError] = useState(''); // 오류 메시지 상태 관리
  const [userData, setUserData] = useState(null); // 사용자 데이터 상태 관리

  useEffect(() => {
    const fetchUserData = async () => {
      if (currentUser) {
        const userDoc = doc(db, 'users', currentUser.uid);
        const docSnapshot = await getDoc(userDoc);
        if (docSnapshot.exists()) {
          setUserData(docSnapshot.data());
        }
      }
    };
    fetchUserData();
  }, [currentUser]);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error("Failed to log out", error);
    }
  };

  const handleImageChange = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('profileImage', file); // 'profileImage'는 서버가 기대하는 필드명

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_HOST}/users/update-profile-picture`, {
        method: 'POST',
        body: formData, // 별도의 Content-Type 헤더를 설정X (브라우저가 알아서 설정)
      });
      const data = await response.json();
      if (response.ok) {
        setProfileImg(data.imageUrl); // 백엔드에서 반환된 이미지 URL로 상태 업데이트
      } else {
        setError(data.error_msg || 'Image upload failed.'); // 백엔드에서 오류 메시지 받기
      }
    } catch (error) {
      setError('Connection to server failed.');
    }
  };

  return (
    <div className="profile-container">
      <header className="main-header">
        GPA
      </header>
      <NavigationBar />
      <h1 className="section-header">Profile</h1>
      <label htmlFor="imageUpload" className="profile-pic-container">
        <img src={profileImg} alt="Profile" className="profile-pic" />
        <input type="file" id="imageUpload" style={{ display: 'none' }} onChange={handleImageChange} accept="image/*" />
      </label>
      {error && <div className="error-message">{error}</div>}
      {/*공백문자*/}
      <div>ㅤ</div>
      {userData && (
        <>
          <p>School: {userData.school}</p>
          <p>Grade: {userData.classnum}</p>
          <p>Name: {userData.name}</p>
        </>
      )}
      {currentUser && <p>Email: {currentUser.email}</p>}
      <div className="element"></div>

      <h2 className="section-header">Account</h2>
      <button className="button" onClick={() => navigate('/ChangeProfile')}>Edit Profile</button>
      <button className="button" onClick={() => navigate('/PasswordChange')}>Change Password</button>

      <div className="element"></div>

      <h2 className="section-header">Information</h2>
      <button className="button" onClick={() => navigate('/ContactAdmin')}>Administrator Contact</button>
      <button className="button" onClick={() => navigate('/LeaveMembership')}>Delete Account</button>
      <button className="button" onClick={handleLogout}>Logout</button>

      {/*공백문자*/}
      <div>ㅤ</div>
    </div>
  );
}

export default ProfilePage;
