import React, { useState } from 'react';
import NavigationBar from './NavigationBar'; // 네비게이션 바
import './css/MainHome.css'; // 메인 홈 페이지 스타일 import
import CourseList from './CourseList';
import { useAuth } from './AuthContext';

const CurrentGPA = () => {
  const { currentUser } = useAuth();
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [selectedSemester, setSelectedSemester] = useState('');

  const handleSelectDepartment = (event) => {
    setSelectedDepartment(event.target.value);
  };

  const handleSelectSemester = (event) => {
    setSelectedSemester(event.target.value);
  };

  return (
    <div className="main-home-container">
      <header className="main-header">
        GPA
      </header>
      <div className="main-content">
        <div className="selector-container">
          <h2>Select Department</h2>
          <select onChange={handleSelectDepartment} value={selectedDepartment}>
            <option value="">Select</option>
            <option value="Computer Science">Computer Science</option>
            <option value="Economics and Trade">Economics and Trade</option>
          </select>
          <h2>Select Semester</h2>
          <select onChange={handleSelectSemester} value={selectedSemester}>
            <option value="">Select</option>
            <option value="2021-2022-1">2021-2022-1</option>
            <option value="2021-2022-2">2021-2022-2</option>
            <option value="2021-2022-3">2021-2022-3</option>
            <option value="2022-2023-1">2022-2023-1</option>
            <option value="2022-2023-2">2022-2023-2</option>
            <option value="2022-2023-3">2022-2023-3</option>
            <option value="2023-2024-1">2023-2024-1</option>
            <option value="2023-2024-2">2023-2024-2</option>
            <option value="2023-2024-3">2023-2024-3</option>
            <option value="2024-2025-1">2024-2025-1</option>
            <option value="2024-2025-2">2024-2025-2</option>
          </select>
        </div>
        {selectedDepartment && selectedSemester && (
          <CourseList userId={currentUser.uid} department={selectedDepartment} semester={selectedSemester} />
        )}
      </div>
      <NavigationBar />
    </div>
  );
};

export default CurrentGPA;
