import React, { useState } from 'react';
import './LoginForm.css'; // 스타일 시트 임포트

function LoginForm({ onLogin }) {
  const [email, setEmail] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onLogin(email);
  };

  return (
    <div className="login-container">
      <div className="title-container">
        <h1 className="title">Everytime</h1>
        <p className="subtitle">for Foreign</p>
      </div>
      <div>
        <h3 style={{textAlign:'center',margin:0}}>회원가입을 진행해주세요!</h3>
        <h5 style={{marginTop:0}}>학교 이메일을 통해서 회원가입을 하실 수 있습니다!</h5>
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
        <button type="submit" className="login-button">
          회원가입
        </button>
      </form>
      <div className="links-container">
      </div>
      <div className="footer">
        <span className="footer-text">
          By clicking continue, you agree to our Terms of Service and Privacy Policy
        </span>
      </div>
      <div className="footer-links">
        <a href="/inquiry" className="auth-link">문의하기</a>
        <a href="/privacy-policy" className="auth-link">개인정보 처리방침</a>
        <a href="/terms-and-conditions" className="auth-link">이용약관</a>
      </div>
    </div>
  );
}

export default LoginForm;
