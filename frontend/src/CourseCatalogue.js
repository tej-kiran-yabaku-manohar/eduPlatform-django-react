import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './CourseCatalogue.css';

function CourseCatalogue() {
  const [filter, setFilter] = useState('');
  const [minRating, setMinRating] = useState(3);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  const handleFilterChange = (event) => {
    setFilter(event.target.value);
  };

  const handleRatingChange = (event) => {
    setMinRating(event.target.value);
  };

  const allCourses = location.state?.allCourses || [];
  console.log('All Courses at catalogue page:', allCourses);

  const enrolledCourses = location.state?.enrolledCourses || [];
  console.log('Enrolled Courses at catalogue page:', enrolledCourses);

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  return (
    <div className="container">
      <h1>Course Catalogue</h1>
      <div className="filter-search-container">
        <input 
          type="text" 
          placeholder="Search courses" 
          value={searchTerm} 
          onChange={handleSearchChange} 
          className="search-bar"
        />
      <div>
        <label htmlFor="filter">Filter by difficulty:</label>
        <select id="filter" value={filter} onChange={handleFilterChange} className="select-filter">
          <option value="">All</option>
          <option value="Beginner">Beginner</option>
          <option value="Intermediate">Intermediate</option>
          <option value="Advanced">Advanced</option>
        </select>
      </div>
      <div>
        <label htmlFor="rating">Minimum Rating: {minRating} Stars</label>
        <input type="range" id="rating" min="1" max="5" value={minRating} onChange={handleRatingChange} step="1" className="rating-slider"/>
      </div>
      </div>
      <div className="allCourses">
        {allCourses.filter(course => course.difficulty.includes(filter) && course.averageRating >= minRating).map(course => (
          <div key={course.id} className="course">
            <img src={course.image} alt={`Course on ${course.name}`} />
            <h3>{course.name}</h3>
            <p>{course.description}</p>
            <button className="view-button" onClick={() => navigate('/course-detail', { state: { course, enrolledCourses} })}>View</button>
          </div>
        ))}
      </div>
    </div>
  );
  
}

export default CourseCatalogue;