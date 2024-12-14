import React from 'react';
import { Link } from 'react-router-dom';
<<<<<<< HEAD
import { Box, List, ListItem, ListItemText, ListItemIcon } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import SchoolIcon from '@mui/icons-material/School';
import AssignmentIcon from '@mui/icons-material/Assignment';
=======
import { Box, List, ListItem, ListItemText } from '@mui/material';
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)

const Sidebar = () => {
  const defaultListItemTextProps = {
    primaryTypographyProps: {
      fontSize: '1.0rem',
<<<<<<< HEAD
      color: '#555555'
    }
=======
      color: '#555555',
    },
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)
  };

  const interviewMeTextProps = {
    primaryTypographyProps: {
      fontWeight: 'bold',
      fontSize: '1.2rem',
<<<<<<< HEAD
      color: '#555555'
    }
  };

  const iconStyle = {
    color: '#555555',
    marginRight: '10px'
=======
      color: '#555555',
    },
  };

  const emojiStyle = {
    fontSize: '1.5rem',
    marginRight: '10px',
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)
  };

  return (
    <Box
      sx={{
        width: '250px',
<<<<<<< HEAD
        height: '100%', 
        backgroundColor: '#f5f5f5',
        padding: '10px',
        borderRight: '1px solid #ddd',
        margin: 0, 
      }}
    >
      <List sx={{ padding: 0 }}> 
      <ListItem
        component={Link}
        sx={{
          padding: '10px',
          borderRadius: '8px',
          cursor: 'pointer',
          '&:hover': {
            backgroundColor: '#f5f5f5',
          },
        }}
      >
        <ListItemText 
          primary="InterviewMe" 
          {...interviewMeTextProps}
        />
      </ListItem>
=======
        height: '100%',
        backgroundColor: '#f5f5f5',
        padding: '10px',
        borderRight: '0px solid #ddd',
        margin: 0,
      }}
    >
      <List sx={{ padding: 0 }}>
        <ListItem
          component={Link}
          sx={{
            padding: '10px',
            borderRadius: '8px',
            cursor: 'pointer',
            '&:hover': {
              backgroundColor: '#f5f5f5',
            },
          }}
        >
          <ListItemText primary="InterviewMe" {...interviewMeTextProps} />
        </ListItem>
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)
        <ListItem
          component={Link}
          to="/chat"
          sx={{
<<<<<<< HEAD
=======
            display: 'flex',
            alignItems: 'center',
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)
            padding: '10px',
            borderRadius: '8px',
            cursor: 'pointer',
            '&:hover': {
              backgroundColor: '#e0e0e0',
            },
          }}
        >
<<<<<<< HEAD
          <ListItemIcon>
            <ChatIcon sx={iconStyle} />
          </ListItemIcon>
          <ListItemText 
            primary="Chat" 
            {...defaultListItemTextProps}
          />
        </ListItem>
        <ListItem
          component={Link}
          to="/courses"
          sx={{
=======
          <span style={emojiStyle}>💬</span> {/* Chat Emoji */}
          <ListItemText primary="Chat" {...defaultListItemTextProps} />
        </ListItem>
        <ListItem
          component={Link}
          to="/mock-space"
          sx={{
            display: 'flex',
            alignItems: 'center',
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)
            padding: '10px',
            borderRadius: '8px',
            cursor: 'pointer',
            '&:hover': {
              backgroundColor: '#e0e0e0',
            },
          }}
        >
<<<<<<< HEAD
          <ListItemIcon>
            <SchoolIcon sx={iconStyle} />
          </ListItemIcon>
          <ListItemText 
            primary="Courses" 
            {...defaultListItemTextProps}
          />
        </ListItem>
        <ListItem
          component={Link}
          to="/prep-plans"
          sx={{
=======
          <span style={emojiStyle}>🎭</span> {/* MockSpace Emoji */}
          <ListItemText primary="MockSpace" {...defaultListItemTextProps} />
        </ListItem>
        <ListItem
          component={Link}
          to="/upload"
          sx={{
            display: 'flex',
            alignItems: 'center',
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)
            padding: '10px',
            borderRadius: '8px',
            cursor: 'pointer',
            '&:hover': {
              backgroundColor: '#e0e0e0',
            },
          }}
        >
<<<<<<< HEAD
          <ListItemIcon>
            <AssignmentIcon sx={iconStyle} />
          </ListItemIcon>
          <ListItemText 
            primary="Prep Plans" 
            {...defaultListItemTextProps}
          />
=======
          <span style={emojiStyle}>📄</span>
          <ListItemText primary="Document Upload" {...defaultListItemTextProps} />
>>>>>>> b2cd094 (Initial commit: Document upload functionality with error handling)
        </ListItem>
      </List>
    </Box>
  );
};

export default Sidebar;
