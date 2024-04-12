import React, { useState } from 'react';
import './RegisterForm.css'; // 스타일 시트 임포트

function RegisterForm({ onLogin }) {
  const [name, setName] = useState('');
  const [birth, setBirth] = useState('');
  const [uni, setUni] = useState('');
  const [uninum, setUninum] = useState('');
  const [major, setMajor] = useState('');
  const [wechat, setWechat] = useState('');
  const [phonenum, setPhonenum] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onLogin(name,birth,uni,uninum,major,wechat,phonenum);
  };

  return (
    <div className="register-container">
      <div className="title-container">
        <h1 className="title">Everytime</h1>
        <p className="subtitle">for Foreign</p>
      </div>
      <form onSubmit={handleSubmit} className="register-form"> 
        <input
          type="name"
          className="register-input"
          placeholder="이름"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="birth"
          className="register-input"
          placeholder="생년월일"
          value={birth}
          onChange={(e) => setBirth(e.target.value)}
          required
        />
        <input
          type="uni"
          className="register-input"
          placeholder="학교"
          value={uni}
          onChange={(e) => setUni(e.target.value)}
          required
        />
        <input
          type="uninum"
          className="register-input"
          placeholder="학번"
          value={uninum}
          onChange={(e) => setUninum(e.target.value)}
          required
        />
        <input
          type="major"
          className="register-input"
          placeholder="과"
          value={major}
          onChange={(e) => setMajor(e.target.value)}
          required
        />
        <input
          type="wechat"
          className="register-input"
          placeholder="위챗"
          value={wechat}
          onChange={(e) => setWechat(e.target.value)}
          required
        />
        <input
          type="phonenum"
          className="register-input"
          placeholder="전화번호"
          value={phonenum}
          onChange={(e) => setPhonenum(e.target.value)}
          required
        />

        <button type="submit" className="register-button">
          회원가입 완료!
        </button>
      </form>
      <div className="links-container">
      </div>
      <div className="footer">
        <span className="footer-text">
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

export default RegisterForm;
