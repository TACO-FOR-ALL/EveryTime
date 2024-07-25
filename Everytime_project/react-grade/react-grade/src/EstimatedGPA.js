import React, { useEffect, useState } from 'react';
import { db } from './firebase';
import { collection, getDocs } from 'firebase/firestore';
import './css/EstimatedGPA.css';
import NavigationBar from './NavigationBar';
import { useAuth } from './AuthContext';

const calculateGPA = (score) => {
  if (score >= 90) return 4.0;
  if (score >= 85) return 3.7;
  if (score >= 80) return 3.4;
  if (score >= 75) return 3.0;
  if (score >= 70) return 2.4;
  if (score >= 65) return 2.0;
  if (score >= 60) return 1.0;
  return 0.0;
};

const calculateAverageGPA = (courses) => {
  if (courses.length === 0) return 0;

  let totalPoints = 0;
  let totalCredits = 0;

  courses.forEach(course => {
    if (course.점수 !== 'N/A' && course.점수 !== '' && course.점수 !== ' ' && course.점수 !== '0') {
        if(course.점수 > 0 ) {
        const score = parseFloat(course.점수);
        const gpa = calculateGPA(score);
        const credits = parseFloat(course.학점);
        totalPoints += gpa * credits;
        totalCredits += credits;
      }
    }
  });

  return totalCredits === 0 ? 0 : (totalPoints / totalCredits).toFixed(2);
};

const EstimatedGPA = () => {
  const { currentUser } = useAuth();
  const userId = currentUser.uid;
  const department = localStorage.getItem('selectedDepartment');
  const [coursesBySemester, setCoursesBySemester] = useState({});
  const [estimatedGPA, setEstimatedGPA] = useState(0);

  useEffect(() => {
    if (!userId || !department) {
      console.error('Missing userId or department');
      return;
    }

    const fetchCourses = async () => {
      const semesters = ['2021-2022-1', '2021-2022-2', '2021-2022-3', '2022-2023-1', '2022-2023-2', '2022-2023-3', '2023-2024-1', '2023-2024-2', '2023-2024-3', '2024-2025-1', '2024-2025-2'];
      let allCoursesBySemester = {};

      try {
        const fetchSemesterCourses = async (semester) => {
          const semesterRef = collection(db, `users/${userId}/departments/${department}/${semester}`);
          const semesterSnap = await getDocs(semesterRef);
          const semesterCourses = semesterSnap.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
          }));
          allCoursesBySemester[semester] = semesterCourses;
        };

        await Promise.all(semesters.map(semester => fetchSemesterCourses(semester)));

        console.log('Fetched courses:', allCoursesBySemester);
        setCoursesBySemester(allCoursesBySemester);
        const allCourses = Object.values(allCoursesBySemester).flat();
        setEstimatedGPA(calculateAverageGPA(allCourses));
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    };

    fetchCourses();
  }, [userId, department]);

  const handleScoreChange = (semester, index, newScore) => {
    const updatedCoursesBySemester = { ...coursesBySemester };
    updatedCoursesBySemester[semester][index].점수 = newScore;
    setCoursesBySemester(updatedCoursesBySemester);

    const allCourses = Object.values(updatedCoursesBySemester).flat();
    setEstimatedGPA(calculateAverageGPA(allCourses));
  };

  return (
    <div className="estimated-gpa-container">
      <header className="estimated-gpa-header">
        Estimated GPA
      </header>
      <h1>{department}</h1>
      <div className="estimated-gpa-content">
        <h2>Current Estimated GPA: {estimatedGPA}</h2>
        {Object.keys(coursesBySemester).map(semester => (
          <div key={semester}>
            <h2>{semester}</h2>
            <table className="course-table">
              <thead>
                <tr>
                  <th>Course Name</th>
                  <th>Credits</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {coursesBySemester[semester].map((course, index) => (
                  <tr key={index}>
                    <td>{course.id}</td>
                    <td>{course.학점}</td>
                    <td>
                      <input 
                        type="number" 
                        value={course.점수} 
                        onChange={(e) => handleScoreChange(semester, index, e.target.value)} 
                        className="input-field"
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
      <NavigationBar />
    </div>
  );
};

export default EstimatedGPA;