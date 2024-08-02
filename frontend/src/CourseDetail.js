import React, { useState, useRef, useEffect} from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './CourseDetail.css';

function CourseDetail() {
  const location = useLocation();
  const navigate = useNavigate();
  const course = location.state?.course;
  const [enrolledCourses, setEnrolledCourses] = useState(location.state?.enrolledCourses || []);
  const [isEnrolled, setIsEnrolled] = useState(enrolledCourses.some(c => c.id === course.id));
  const enrollButtonRef = useRef(null);
  const progress = course?.progress?.replace('%', '') || '0';


  useEffect(() => {
    if (!isEnrolled && enrollButtonRef.current) {
      enrollButtonRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [isEnrolled]);

  console.log('Enrolled Courses at details page:', enrolledCourses);
  console.log('Course selected at details page:', course);

  if (!course) {
    return <div>No course data available.</div>;
  }

  const goToCatalogue = () => {
    fetchAllCourses();
  };

  const fetchAllCourses = () => {
    console.log('Fetching all courses for the catalogue');
    fetch('http://localhost:8000/all-courses/')
      .then(response => response.json())
      .then(data => {
        console.log('All courses at course-detail page:', data);
        navigate('/course-catalogue', { state: { allCourses:data } });
      })
      .catch(error => console.error('Error fetching allCourses:', error));
  };

  const addToDashboard = (course) => {
    console.log('Adding to dashboard:', course);
    fetch('http://localhost:8000/enrolled-courses/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        course_id: course.id,
        name: course.name,
        progress: "0%",
      }),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Course added:', data);
      setEnrolledCourses(prevCourses => [...prevCourses, data]);    
      setIsEnrolled(true);
    })
    .catch(error => console.error('Error adding course:', error));
  };

  const deleteCourse = (course) => {
    fetch(`http://localhost:8000/enrolled-courses/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        course_id: course.id,
      }),
    })
    .then(response => {
      if (response.ok) {
        console.log('Course deleted successfully');
        setIsEnrolled(false);
        setEnrolledCourses(prevCourses => prevCourses.filter(enrolledCourse => enrolledCourse.id !== course.id));
        enrollButtonRef.current.scrollIntoView({ behavior: 'smooth' });
      } else {
        throw new Error('Failed to delete course');
      }
    })
    .catch(error => console.error('Error deleting course:', error));
  };

  const updateProgress = (Id, newProgress) => {
    const updateProgress = `${newProgress}%`;
    fetch(`http://localhost:8000/enrolled-courses/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ course_id: Id, progress: updateProgress})
    })
    .then(response => response.json())
    .then(data => {
      console.log('Update progress successful', data);
    })
    .catch(error => console.error('Error updating course:', error));
  };
  

  return (
    <div className="course-detail-container">
      <div className="button-container">
        <button onClick={goToCatalogue} className="back-button">Back to Course Catalogue</button>
        {/* <button onClick={() => navigate('/')} className="home-button">Home</button> */}
      </div>
      <h1>Course Detail</h1>
      <div className="top-container">
        <h2>Instructor: {course.instructor || 'TBA'}</h2>
        {isEnrolled && (
          <button className="unenroll-button" onClick={() => deleteCourse(course)}>Archive course</button>
        )}
      </div>
      <img src={course.image} alt={`Course on ${course.name}`}/>
      <p>{course.description}</p>
      <h3>Duration: {course.duration}</h3>
      <h3>Syllabus</h3>
      <ul>
        {course.syllabus?.map((item, index) => (
          <li key={index}>{item}</li>
        )) || <li>No syllabus available.</li>}
      </ul>
      <h3>Choose Your Session Timing:</h3>
      <div>
        <input type="radio" id="morning" name="session-time" value="Morning" />
        <label htmlFor="morning">Morning</label>
        <input type="radio" id="afternoon" name="session-time" value="Afternoon" />
        <label htmlFor="afternoon">Afternoon</label>
        <input type="radio" id="evening" name="session-time" value="Evening" />
        <label htmlFor="evening">Evening</label>
      </div>
      <div className = "progress-update">
        <div style={{ marginTop: '80px' }}></div>
        <div style={{ marginLeft: '-30px' }}></div>
        <div style={{ marginBottom: '20px' }}></div>
        <label><h3>Progress:</h3> {course.progress}</label>
        <input
          type="range"
          min="0"
          max="100"
          defaultValue={progress}
          onChange={event => { 
            console.log(`Current Progress: ${event.target.value}%`);
          }}
        />
        <button onClick={(e) => {
          const input = e.target.previousElementSibling;
          updateProgress(course.id, input.value);
        }}>
          Update
        </button>
      </div>
      <div style={{ marginBottom: '-20px' }}></div>
      <h3>Reviews</h3>
      <input type="text" placeholder="Search reviews" className="search-reviews" />
      <div className="review-container">
        {course.reviews?.length > 0 ? course.reviews.map((review, index) => (
          <div key={index} className="review">
            <p><strong>{review.reviewer}</strong> says: {review.comment}</p>
          </div>
        )) : <div>No reviews available.</div>}
      </div>
      
      
      {isEnrolled ? (
        <div className="enrollment-message">
          <p>You have successfully enrolled in this course.</p>
          <button className="view-button" onClick={() => navigate('/')}>Go to Dashboard</button>
        </div>
      ) : (
        <button ref={enrollButtonRef} className="enroll-button" onClick={() => addToDashboard(course)}>Enroll Now</button>
      )}
    </div>
  );
}

export default CourseDetail;
