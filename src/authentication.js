import React, { useState } from 'react';
import './LoginForm.css'; // 스타일 시트 임포트

function LoginForm({ onLogin }) {
  const [authentication, setAuthentication] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onLogin(authentication);
  };

  return (
    <div className="login-container">
      <div className="title-container">
        <h1 className="title">Everytime</h1>
        <p className="subtitle">for Foreign</p>
      </div>
      <div>
        <h3 style={{textAlign:'center',margin:0}}>인증번호가 학교이메일에 도착했습니다!</h3>
        <h5 style={{marginTop:0,textAlign:'center'}}>학교 이메일에서 인증번호를 확인해주세요!</h5>
        </div>
      <form onSubmit={handleSubmit} className="login-form"> 
        <input
          type="authentication"
          className="login-input"
          placeholder="인증번호를 입력해주세요!(제한시간: 5분)"
          value={authentication}
          onChange={(e) => setAuthentication(e.target.value)}
          required
        />
        <button type="submit" className="login-button">
          인증번호 확인!
        </button>
      </form>
      <div className="links-container">
      </div>
      <div className="footer">
        <span className="footer-text">
          *인증번호가 틀리다면 학교이메일이 정확한지 확인해주세요!
        </span>
      </div>
      <div className="footer-links">
      </div>
    </div>
  );
}

export default LoginForm;