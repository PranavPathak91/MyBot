import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Card, CardContent, LinearProgress, Chip, Grid, IconButton, Tooltip } from '@mui/material';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import MenuBookOutlinedIcon from '@mui/icons-material/MenuBookOutlined';

const CoursesPage = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);

  // Simulate fetching data from the backend
  useEffect(() => {
    const fetchCourses = async () => {
      const placeholderCourses = [
        {
          id: 1,
          title: 'Frontend Development Bootcamp',
          description: 'Learn React, JavaScript, and web development fundamentals.',
          progress: 65,
          keySkills: ['React', 'JavaScript', 'HTML', 'CSS'],
        },
        {
          id: 2,
          title: 'Data Science Essentials',
          description: 'Introduction to Python, data analysis, and machine learning.',
          progress: 80,
          keySkills: ['Python', 'Pandas', 'Machine Learning'],
        },
        {
          id: 3,
          title: 'UI/UX Design Basics',
          description: 'Design principles, wireframing, and prototyping techniques.',
          progress: 30,
          keySkills: ['Design Principles', 'Figma', 'Prototyping'],
        },
        {
          id: 4,
          title: 'Cloud Computing Fundamentals',
          description: 'Explore cloud services like AWS, Azure, and Google Cloud.',
          progress: 50,
          keySkills: ['AWS', 'Azure', 'Google Cloud'],
        },
      ];

      setCourses(placeholderCourses);
    };

    fetchCourses();
  }, []);

  const openPrepPlan = (courseId) => {
    navigate(`/prep-plans/${courseId}`);
  };

  const openChat = (courseId) => {
    navigate(`/chat/${courseId}`);
  };

  return (
    <Box
      sx={{
        padding: '20px 50px',
        backgroundColor: '#f8f9fa',
        height: '90vh',
        overflowY: 'auto', // Enable scrolling
        scrollbarWidth: 'none', // Hide scrollbar for Firefox
        '-ms-overflow-style': 'none', // Hide scrollbar for IE and Edge
        '&::-webkit-scrollbar': {
          display: 'none', // Hide scrollbar for Chrome, Safari, and newer Edge
        },
      }}
    >
      {/* Header */}
      <Typography variant="h4" sx={{ textAlign: 'center', fontWeight: 'bold', marginBottom: '20px' }}>
        Active Courses
      </Typography>

      {/* Course Grid */}
      <Grid container spacing={4}>
        {courses.map((course) => (
          <Grid item xs={12} sm={6} md={4} key={course.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                backgroundColor: '#ffffff',
                borderRadius: '10px',
                boxShadow: 1,
                '&:hover': {
                  boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
                },
              }}
            >
              <CardContent
                sx={{
                  flexGrow: 1,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                }}
              >
                {/* Title and Description */}
                <Box sx={{ minHeight: '120px' /* Adjust height to align progress bars */ }}>
                  <Typography
                    variant="h6"
                    sx={{ fontWeight: 'bold', marginBottom: '10px', fontSize: '1.2rem' }}
                  >
                    {course.title}
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#666', marginBottom: '15px' }}>
                    {course.description}
                  </Typography>
                </Box>

                {/* Key Skills */}
                <Box
                  sx={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '10px',
                    minHeight: '60px', // Adjust height for consistent alignment
                    marginBottom: '15px',
                  }}
                >
                  {course.keySkills.map((skill, index) => (
                    <Chip
                      key={index}
                      label={skill}
                      sx={{
                        backgroundColor: '#f0f0f0',
                        color: '#333',
                        fontWeight: 'bold',
                        fontSize: '0.85rem',
                      }}
                    />
                  ))}
                </Box>

                {/* Progress Bar */}
                <Box sx={{ marginBottom: '15px' }}>
                  <Typography variant="body2" sx={{ marginBottom: '5px' }}>
                    Completion: {course.progress}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={course.progress}
                    sx={{
                      height: '8px',
                      borderRadius: '5px',
                      backgroundColor: '#f0f0f0',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: '#4CAF50', // Green progress bar
                      },
                    }}
                  />
                </Box>

                {/* Buttons */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', marginTop: 'auto' }}>
                  <Tooltip title="Chat" arrow>
                    <IconButton
                      sx={{
                        border: '1px solid black',
                        borderRadius: '10px',
                        color: 'black',
                      }}
                      onClick={() => openChat(course.id)}
                    >
                      <ChatBubbleOutlineIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Prep Plan" arrow>
                    <IconButton
                      sx={{
                        border: '1px solid black',
                        borderRadius: '10px',
                        color: 'black',
                      }}
                      onClick={() => openPrepPlan(course.id)}
                    >
                      <MenuBookOutlinedIcon />
                    </IconButton>
                  </Tooltip>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default CoursesPage;
