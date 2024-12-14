import React from 'react';
import { useLocation } from 'react-router-dom';
import { Box, Typography, Avatar } from '@mui/material';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import Sidebar from '../components/common/Sidebar';

const MainLayout = ({ children }) => {
  const location = useLocation();

  // Map routes to page titles
  const getPageTitle = () => {
    switch (location.pathname) {
      case '/chat':
        return 'Prep Hub';
      case '/courses':
        return 'Courses';
      case '/prep-plans':
        return 'Prep Plans';
      default:
        return 'Welcome';
    }
  };

  return (
    <Box 
      sx={{ 
        display: 'flex', 
        height: '100vh', 
        width: '100%', 
        margin: 0, 
        padding: 0, 
        overflow: 'hidden',
        boxSizing: 'border-box'
      }}
    >
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <Box sx={{ 
        flex: 1, 
        display: 'flex', 
        flexDirection: 'column',
        margin: 0,
        padding: 0,
        overflow: 'hidden',
        width: '100%',
        height: '100%',
        boxSizing: 'border-box'
      }}>
        {/* Header */}
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '10px 20px',
<<<<<<< HEAD
            borderBottom: '1px solid #ddd',
=======
            borderBottom: '0px solid #ddd',
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)
            backgroundColor: '#ffffff',
            height: '60px', // Fixed height for header
            minHeight: '60px',
            width: '100%',
            boxSizing: 'border-box'
          }}
        >
          {/* Page Title with Dropdown Icon */}
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography
              variant="h5"
              component="h1"
              sx={{ fontWeight: 600, fontSize: '20px', marginRight: '5px' }}
            >
              {getPageTitle()}
            </Typography>
          </Box>

          {/* User Avatar */}
          <Avatar 
            alt="User Avatar" 
            src="/path/to/avatar.jpg" 
            sx={{ width: 40, height: 40 }} 
          />
        </Box>

        {/* Page Content */}
        <Box sx={{ 
          flex: 1, 
          overflow: 'hidden', 
          padding: '20px 50px',
          margin: 0,
          width: '95%',
          boxSizing: 'border-box'
        }}>
          {children}
        </Box>
      </Box>
    </Box>
  );
};

export default MainLayout;