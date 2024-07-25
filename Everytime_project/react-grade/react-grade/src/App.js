// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './LoginForm';
import PasswordResetPage from './PasswordResetPage';
import RegisterForm from './RegisterForm';
import ProfilePage from './ProfilePage';
import PasswordChange from './PasswordChange';
import LeaveMembership from './LeaveMembership';
import ContactAdmin from './ContactAdmin';
import ChangeProfile from './ChangeProfile';
import MainHome from './MainHome';
import CurrentGPA from './CurrentGPA';
import EstimatedGPA from './EstimatedGPA';
import { AuthProvider } from './AuthContext';
import ProtectedRoute from './ProtectedRoute';
import '@fortawesome/fontawesome-free/css/all.min.css';

function App() {
  const handleLogin = (id, password) => {
    // TODO: 여기에 로그인 처리 로직 구현
    console.log('Login attempt:', id, password);
  };

  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Navigate replace to="/login" />} />
          {/* 루트 경로를 로그인 페이지로 리다이렉트 */}
          <Route path="/login" element={<LoginForm onLogin={handleLogin} />} />
          <Route path="/PasswordResetPage" element={<PasswordResetPage />} />
          <Route path="/RegisterForm" element={<RegisterForm onLogin={handleLogin} />} />
          <Route
            path="/ProfilePage"
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/PasswordChange"
            element={
              <ProtectedRoute>
                <PasswordChange />
              </ProtectedRoute>
            }
          />
          <Route
            path="/LeaveMembership"
            element={
              <ProtectedRoute>
                <LeaveMembership />
              </ProtectedRoute>
            }
          />
          <Route
            path="/ContactAdmin"
            element={
              <ProtectedRoute>
                <ContactAdmin />
              </ProtectedRoute>
            }
          />
          <Route
            path="/ChangeProfile"
            element={
              <ProtectedRoute>
                <ChangeProfile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/MainHome"
            element={
              <ProtectedRoute>
                <MainHome />
              </ProtectedRoute>
            }
          />
          <Route
            path="/CurrentGPA"
            element={
              <ProtectedRoute>
                <CurrentGPA />
              </ProtectedRoute>
            }
          />
          <Route
            path="/EstimatedGPA"
            element={
              <ProtectedRoute>
                <EstimatedGPA />
              </ProtectedRoute>
            }
          />
          {/* 추가 라우트 여기에 정의 / 아래는 네이게이션 바 설정칸 */}
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;