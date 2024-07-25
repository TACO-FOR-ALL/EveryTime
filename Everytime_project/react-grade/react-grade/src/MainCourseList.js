import React, { useEffect, useState } from 'react';
import { db } from './firebase';
import { collection, getDocs } from 'firebase/firestore';
import './css/CourseList.css';

function MainCourseList({ department, userId, onUpdateAverageGPA }) {
  const [coursesBySemester, setCoursesBySemester] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      if (!department) return;

      try {
        console.log(`Fetching courses for department: ${department}`);
        setLoading(true);

        const semesters = ['2021-2022-1', '2021-2022-2', '2021-2022-3', '2022-2023-1', '2022-2023-2', '2022-2023-3', '2023-2024-1', '2023-2024-2', '2023-2024-3', '2024-2025-1', '2024-2025-2'];

        const fetchSemesterCourses = async (semester) => {
          const semesterRef = collection(db, `users/${userId}/departments/${department}/${semester}`);
          const semesterSnap = await getDocs(semesterRef);
          const semesterCourses = semesterSnap.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
          }));
          return { semester, semesterCourses };
        };

        const fetchAllCourses = async () => {
          const promises = semesters.map(fetchSemesterCourses);
          const results = await Promise.all(promises);
          let allCoursesBySemester = {};
          results.forEach(({ semester, semesterCourses }) => {
            allCoursesBySemester[semester] = semesterCourses;
          });
          return allCoursesBySemester;
        };

        const allCourses = await fetchAllCourses();
        console.log('Fetched courses:', allCourses);
        setCoursesBySemester(allCourses);
        setLoading(false);
        calculateAverageGPA(allCourses);
      } catch (error) {
        console.error('Error fetching courses:', error);
        setLoading(false);
      }
    };

    fetchCourses();
  }, [department, userId]);

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

  const calculateAverageGPA = (coursesBySemester) => {
    let totalPoints = 0;
    let totalCredits = 0;

    for (const semester in coursesBySemester) {
      coursesBySemester[semester].forEach(course => {
        if (course.점수 !== 'N/A' && course.점수 !== '' && course.점수 !== ' ' && course.점수 !== '0') {
          if(course.점수 > 0 ){
            const score = parseFloat(course.점수);
            const gpa = calculateGPA(score);
            const credits = parseFloat(course.학점);
            totalPoints += gpa * credits;
            totalCredits += credits;
          }
        }
      });
    }

    const average = totalCredits === 0 ? 0 : totalPoints / totalCredits;
    onUpdateAverageGPA(average.toFixed(2));
  };

  return (
    <div>
      <h1>{department}</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        Object.keys(coursesBySemester).map(semester => (
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
                    <td>{course.점수 !== 'N/A' ? course.점수 : ''}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))
      )}
    </div>
  );
}

export default MainCourseList;