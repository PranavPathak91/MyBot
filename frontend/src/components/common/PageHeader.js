import React from 'react';
import { Box, Typography } from '@mui/material';

const PageHeader = ({ title, action }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '20px 0',
        borderBottom: '1px solid #ddd',
        marginBottom: '20px',
      }}
    >
      <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
        {title}
      </Typography>
      {action && <Box>{action}</Box>}
    </Box>
  );
};

export default PageHeader;