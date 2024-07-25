import React, { useEffect, useState } from 'react';
import './css/MainHome.css';
import NavigationBar from './NavigationBar';
import './css/CurrentGPA.css'; 
import MainCourseList from './MainCourseList';
import { useAuth } from './AuthContext';

const MainHome = () => {
  const { currentUser } = useAuth();
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [averageGPA, setAverageGPA] = useState(0);

  useEffect(() => {
    // localStorage에서 선택된 학과를 가져옴
    const savedDepartment = localStorage.getItem('selectedDepartment');
    if (savedDepartment) {
      setSelectedDepartment(savedDepartment);
    }
  }, []);

  const handleSelectDepartment = (event) => {
    const department = event.target.value;
    setSelectedDepartment(department);
    // localStorage에 선택된 학과를 저장
    localStorage.setItem('selectedDepartment', department);
  };

  const handleUpdateAverageGPA = (gpa) => {
    setAverageGPA(gpa);
  };

  return (
    <div className="main-home-container">
      <header className="main-header">
        GPA
      </header>
      <div className="main-text">
        <p>You can look up your grades here.</p>
        <p>If nothing pops up, please go to the Score Correction Page and enter your score.</p>
      </div>
      <div className="main-content">
        <div className="selector-container">
          <h2>Select Department</h2>
          <select onChange={handleSelectDepartment} value={selectedDepartment}>
            <option value="">Select</option>
            <option value="Computer Science">Computer Science</option>
            <option value="Economics and Trade">Economics and Trade</option>
          </select>
        </div>
        <h2>Average GPA: {averageGPA}</h2>
        {selectedDepartment && (
          <MainCourseList userId={currentUser.uid} department={selectedDepartment} onUpdateAverageGPA={handleUpdateAverageGPA} />
        )}
      </div>
      <NavigationBar />
    </div>
  );
};

export default MainHome;