// LoginForm.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // react-router-dom의 Link 컴포넌트를 임포트합니다
import './LoginForm.css'; // LoginForm 스타일 시트 임포트

function LoginForm({ onLogin }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
  
    const handleSubmit = (event) => {
      event.preventDefault();
      onLogin(email, password); // onLogin prop 호출
    };

  return (
    <div className="login-container">
      <div className="title-container">
        <h1 className="title">Everytime</h1>
        <p className="subtitle">for Foreign</p>
      </div>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="email"
          className="login-input"
          placeholder="이메일"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          className="login-input"
          placeholder="비밀번호"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" className="login-button">
          에브리타임 로그인
        </button>
      </form>
      <div className="links-container">
        {/* React Router의 Link 컴포넌트를 사용하여 페이지 내부에서의 이동을 처리 */}
        <Link to="/password-reset" className="auth-link">회원가입</Link>
        {/*이 LINK 부분 회원가입 모듈 삽입 후 수정하기 */}
        <Link to="/password-reset" className="auth-link">비밀번호 찾기</Link>
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