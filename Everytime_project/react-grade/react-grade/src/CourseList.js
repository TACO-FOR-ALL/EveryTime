import React, { useEffect, useState } from 'react';
import { db } from './firebase';
import { collection, doc, getDocs, setDoc } from 'firebase/firestore';
import './css/CourseList.css';

function CourseList({ department, semester, userId }) {
  const [courses, setCourses] = useState([]);
  const [editing, setEditing] = useState(null);
  const [newScore, setNewScore] = useState('');
  const [newCourse, setNewCourse] = useState({ 수업명: '', 학점: '', 점수: '' });

  useEffect(() => {
    const fetchCourses = async () => {
      if (!department || !semester) return;

      try {
        console.log(`Fetching courses for department: ${department}, semester: ${semester}`);
        const userCoursesRef = collection(db, 'users', userId, 'departments', department, semester);
        const userCoursesSnap = await getDocs(userCoursesRef);
        let coursesList = userCoursesSnap.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }));

        if (coursesList.length === 0) {
          const coursesRef = collection(db, 'courses', department, semester);
          const coursesSnap = await getDocs(coursesRef);
          coursesList = coursesSnap.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
          }));
          // Save initial courses to user collection
          for (const course of coursesList) {
            await setDoc(doc(userCoursesRef, course.id), course);
          }
        }

        console.log('Fetched courses:', coursesList);
        setCourses(coursesList);
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    };

    fetchCourses();
  }, [department, semester, userId]);

  const handleEdit = (index) => {
    setEditing(index);
    setNewScore(courses[index].점수);
  };

  const handleUpdate = async (index) => {
    const updatedCourses = [...courses];
    updatedCourses[index].점수 = newScore || '';
    setCourses(updatedCourses);

    const courseDoc = doc(db, `users/${userId}/departments/${department}/${semester}/${updatedCourses[index].id}`);
    await setDoc(courseDoc, {
      학점: updatedCourses[index].학점,
      점수: newScore || ''
    });

    setEditing(null);
    setNewScore('');
  };

  const handleAddCourse = async () => {
    const newCourseData = {
      학점: newCourse.학점,
      점수: newCourse.점수 || ''
    };

    const courseDoc = doc(db, `users/${userId}/departments/${department}/${semester}/${newCourse.수업명}`);
    await setDoc(courseDoc, newCourseData);

    setCourses([...courses, { id: newCourse.수업명, ...newCourseData }]);
    setNewCourse({ 수업명: '', 학점: '', 점수: '' });
  };

  return (
    <div>
      <h1>{department} - {semester}</h1>
      <table className="course-table">
        <thead>
          <tr>
            <th>Course Name</th>
            <th>Credits</th>
            <th>Score</th>
            <th>Edit</th>
          </tr>
        </thead>
        <tbody>
          {courses.map((course, index) => (
            <tr key={index}>
              <td>{course.id}</td>
              <td>{course.학점}</td>
              <td>
                {editing === index ? (
                  <input 
                    type="number" 
                    value={newScore} 
                    onChange={(e) => setNewScore(e.target.value)} 
                    className="input-field3"
                  />
                ) : (
                  course.점수 || ''
                )}
              </td>
              <td>
                {editing === index ? (
                  <button onClick={() => handleUpdate(index)} className="button">
                    <i className="fas fa-save"></i>
                    </button>
                  ) : (
                    <button onClick={() => handleEdit(index)} className="button">
                      <i className="fas fa-edit"></i>
                    </button>
                  )}
              </td>c
            </tr>
          ))}
        </tbody>
      </table>
      <h2>Add New Course</h2>
      <input
        type="text"
        placeholder="Course Name"
        value={newCourse.수업명}
        onChange={(e) => setNewCourse({ ...newCourse, 수업명: e.target.value })}
        className="input-field"
      />
      <input
        type="number"
        placeholder="Credits"
        value={newCourse.학점}
        onChange={(e) => setNewCourse({ ...newCourse, 학점: e.target.value })}
        className="input-field2"
      />
      <input
        type="number"
        placeholder="Score"
        value={newCourse.점수}
        onChange={(e) => setNewCourse({ ...newCourse, 점수: e.target.value })}
        className="input-field2"
      />
      <button onClick={handleAddCourse} className="button">Add Course</button>
    </div>
  );
}

export default CourseList;
