import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import ChatPage from './pages/ChatPage';
<<<<<<< HEAD
import CoursesPage from './pages/CoursesPage';
import PrepPlansPage from './pages/PrepPlansPage';
=======
import MockSpacePage from './pages/MockSpacePage';
import DocumentUploadPage from './pages/DocumentUploadPage';
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)

const App = () => {
  return (
    <Router>
      <MainLayout>
        <Routes>
          <Route path="/chat" element={<ChatPage />} />
<<<<<<< HEAD
          <Route path="/courses" element={<CoursesPage />} />
          <Route path="/prep-plans" element={<PrepPlansPage />} />
=======
          <Route path="/mock-space" element={<MockSpacePage />} />
          <Route path="/upload" element={<DocumentUploadPage />} />
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)
          <Route path="*" element={<h1>Page Not Found</h1>} />
        </Routes>
      </MainLayout>
    </Router>
  );
};

export default App;