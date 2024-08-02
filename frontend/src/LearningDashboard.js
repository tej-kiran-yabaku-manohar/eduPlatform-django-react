import React, { useState, useEffect} from 'react';
import { useNavigate, } from 'react-router-dom';
import './LearningDashboard.css';

function LearningDashboard() {
  const navigate = useNavigate();
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [allCourses, setAllCourses] = useState([]);

  const goToCatalogue = () => {
    navigate('/course-catalogue', { state: { allCourses, enrolledCourses } });
  };

  const continueLearning = (course) => {
    console.log('Sending correct course details', course);

    const course_Fulldetails = allCourses.find(c => c.id === course.id);
    if (course_Fulldetails){
      console.log('Checking course full details', course_Fulldetails);

      navigate('/course-detail', { state: { course: course_Fulldetails, enrolledCourses } });
    }
    
  };
     

  useEffect(() => {
    fetch('http://localhost:8000/all-courses/')
    // fetch('http://3.138.251.37/all-courses/')
    .then(response => response.json())
    .then(data => setAllCourses(data))
    .catch(error => console.error('Error fetching allCourses:', error));
    }, []);
  console.log('All courses at dashboard page:', allCourses);

  useEffect(() => {
    // fetch('http://3.138.251.37/')
    fetch('http://localhost:8000/enrolled-courses/')
      .then(response => response.json())
      .then(data => setEnrolledCourses(data))
      .catch(error => console.error('Error fetching courses:', error));
  }, []);

  console.log('Enrolled Courses at dashboard page:', enrolledCourses);
 

  return (
    <div className="dashboard-container">
      <h1>Learning Dashboard</h1>
      <p>Welcome to your learning dashboard!</p>
      <p>Manage your courses and progress here.</p>

      <ul>
        {enrolledCourses.map((course) => (
          <li key={course.id} className="course-item">
            <div className="course-title">
              <label htmlFor={`course-${course.id}`}><h2>{course.name}</h2></label>
            </div>
            <p>Progress: {course.progress}</p>
            <button className="progress-button"  onClick={() => continueLearning(course)}>Continue Learning</button>
            <input type="text" placeholder="Add notes..." className="course-notes" />
          </li>
        ))}
      </ul>

      <button onClick={goToCatalogue} className="explore-button">Explore Courses</button>

      <div className="image-container">
        <img src="https://dashboardlearning.com/wp-content/uploads/2022/02/about-dashboard-2.png" alt="Learning Dashboard Overview"/>
      </div>
    </div>
  );
}

export default LearningDashboard;
