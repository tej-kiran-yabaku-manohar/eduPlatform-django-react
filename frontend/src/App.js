import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import CourseCatalogue from './CourseCatalogue';
import CourseDetail from './CourseDetail';
import LearningDashboard from './LearningDashboard';
import './App.css';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={< LearningDashboard/>} />
          <Route path="/course-catalogue" element={<CourseCatalogue />} />
          <Route path="/course-detail" element={<CourseDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
