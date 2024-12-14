import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import ChatPage from './pages/ChatPage';
import MockSpacePage from './pages/MockSpacePage';
import DocumentUploadPage from './pages/DocumentUploadPage';

const App = () => {
  return (
    <Router>
      <MainLayout>
        <Routes>
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/mock-space" element={<MockSpacePage />} />
          <Route path="/upload" element={<DocumentUploadPage />} />
          <Route path="*" element={<h1>Page Not Found</h1>} />
        </Routes>
      </MainLayout>
    </Router>
  );
};

export default App;