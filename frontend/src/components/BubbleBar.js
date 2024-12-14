import React from 'react';
import { Box, Button } from '@mui/material';

const BubbleBar = () => {
  return (
    <Box
      data-component="bubble-bar-container"
      sx={{
        display: 'flex',
        gap: '10px',
        justifyContent: 'center',
        padding: '10px',
        backgroundColor: '#ffffff',
        borderBottom: '1px solid #f0f0f0',
      }}
    >
      {/* Placeholder buttons */}
      <Button
        variant="contained"
        sx={{
          backgroundColor: '#f0f0f0',
          color: '#000',
          textTransform: 'none',
          borderRadius: '20px',
          boxShadow: 'none',
          '&:hover': {
            backgroundColor: '#e0e0e0',
          },
        }}
      >
        🦖 Create image
      </Button>
      <Button
        variant="contained"
        sx={{
          backgroundColor: '#f0f0f0',
          color: '#000',
          textTransform: 'none',
          borderRadius: '20px',
          boxShadow: 'none',
          '&:hover': {
            backgroundColor: '#e0e0e0',
          },
        }}
      >
        Get advice
      </Button>
      <Button
        variant="contained"
        sx={{
          backgroundColor: '#f0f0f0',
          color: '#000',
          textTransform: 'none',
          borderRadius: '20px',
          boxShadow: 'none',
          '&:hover': {
            backgroundColor: '#e0e0e0',
          },
        }}
      >
        📝 Summarize text
      </Button>
      <Button
        variant="contained"
        sx={{
          backgroundColor: '#f0f0f0',
          color: '#000',
          textTransform: 'none',
          borderRadius: '20px',
          boxShadow: 'none',
          '&:hover': {
            backgroundColor: '#e0e0e0',
          },
        }}
      >
        ⚯ Brainstorm
      </Button>
      <Button
        variant="contained"
        sx={{
          backgroundColor: '#f0f0f0',
          color: '#000',
          textTransform: 'none',
          borderRadius: '20px',
          boxShadow: 'none',
          '&:hover': {
            backgroundColor: '#e0e0e0',
          },
        }}
      >
        🍔 More
      </Button>
    </Box>
  );
};

export default BubbleBar;
