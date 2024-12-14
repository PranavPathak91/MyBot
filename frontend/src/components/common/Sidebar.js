import React from 'react';
import { Link } from 'react-router-dom';
import { Box, List, ListItem, ListItemText, ListItemIcon } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import AssignmentIcon from '@mui/icons-material/Assignment';

const Sidebar = () => {
  const defaultListItemTextProps = {
    primaryTypographyProps: {
      fontSize: '1.0rem',
      color: '#555555'
    }
  };

  const interviewMeTextProps = {
    primaryTypographyProps: {
      fontWeight: 'bold',
      fontSize: '1.2rem',
      color: '#555555'
    }
  };

  const iconStyle = {
    color: '#555555',
    marginRight: '10px'
  };

  return (
    <Box
      sx={{
        width: '250px', 
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
          <ListItemText primary="InterviewMe" {...interviewMeTextProps} />
        </ListItem>
        <ListItem
          component={Link}
          to="/chat"
          sx={{
            padding: '10px',
            borderRadius: '8px',
            cursor: 'pointer',
            '&:hover': {
              backgroundColor: '#f5f5f5',
            },
          }}
        >
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
          to="/mock-space"
          sx={{
            padding: '10px',
            borderRadius: '8px',
            cursor: 'pointer',
            '&:hover': {
              backgroundColor: '#f5f5f5',
            },
          }}
        >
          <ListItemIcon>
            <AssignmentIcon sx={iconStyle} />
          </ListItemIcon>
          <ListItemText 
            primary="MockSpace" 
            {...defaultListItemTextProps}
          />
        </ListItem>
        <ListItem
          component={Link}
          to="/upload"
          sx={{
            padding: '10px',
            borderRadius: '8px',
            cursor: 'pointer',
            '&:hover': {
              backgroundColor: '#f5f5f5',
            },
          }}
        >
          <ListItemIcon>
            <AssignmentIcon sx={iconStyle} />
          </ListItemIcon>
          <ListItemText 
            primary="Document Upload" 
            {...defaultListItemTextProps}
          />
        </ListItem>
      </List>
    </Box>
  );
};

export default Sidebar;
