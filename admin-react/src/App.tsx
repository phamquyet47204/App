import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import Departments from './pages/Departments';
import Majors from './pages/Majors';
import Subjects from './pages/Subjects';
import Students from './pages/Students';
import Teachers from './pages/Teachers';
import Grades from './pages/Grades';
import CourseClasses from './pages/CourseClasses';
import Notifications from './pages/Notifications';

import Login from './pages/Login';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }>
          <Route index element={<Dashboard />} />
          <Route path="departments" element={<Departments />} />
          <Route path="majors" element={<Majors />} />
          <Route path="subjects" element={<Subjects />} />
          <Route path="students" element={<Students />} />
          <Route path="teachers" element={<Teachers />} />
          <Route path="grades" element={<Grades />} />
          <Route path="course-classes" element={<CourseClasses />} />
          <Route path="notifications" element={<Notifications />} />

        </Route>
      </Routes>
    </Router>
  );
}

export default App;