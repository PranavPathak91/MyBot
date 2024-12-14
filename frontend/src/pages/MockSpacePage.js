import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  LinearProgress,
  Chip,
  Grid,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

const MockSpacePage = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [courseToDelete, setCourseToDelete] = useState(null);

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

  const handleDeleteCourse = (course) => {
    setCourseToDelete(course);
  };

  const confirmDeleteCourse = () => {
    if (courseToDelete) {
      setCourses((prevCourses) =>
        prevCourses.filter((course) => course.id !== courseToDelete.id)
      );
      setCourseToDelete(null);
    }
  };

  const cancelDeleteCourse = () => {
    setCourseToDelete(null);
  };

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
        backgroundColor: '#ffffff',
        height: '90vh',
        overflowY: 'auto',
        scrollbarWidth: 'none',
        '-ms-overflow-style': 'none',
        '&::-webkit-scrollbar': {
          display: 'none',
        },
      }}
    >
      <Typography
        variant="h4"
        sx={{
          marginBottom: '20px',
          fontWeight: 'bold',
          color: '#333',
        }}
      >
        My Courses
      </Typography>

      <Grid container spacing={3}>
        {courses.map((course) => (
          <Grid item xs={12} sm={6} md={4} key={course.id}>
            <Box
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                backgroundColor: '#f5f5f5',
                borderRadius: '8px',
                overflow: 'hidden',
                position: 'relative',
                '&:hover': {
                  backgroundColor: '#ececec',
                  transform: 'translateY(-5px)',
                },
              }}
            >
              {/* Delete Course Button */}
              <Tooltip title="Delete Course">
                <IconButton
                  onClick={() => handleDeleteCourse(course)}
                  sx={{
                    position: 'absolute',
                    top: 8,
                    right: 8,
                    zIndex: 10,
                    color: 'rgba(0,0,0,0.4)',
                    '&:hover': {
                      color: 'rgba(0,0,0,0.7)',
                    },
                  }}
                >
                  <CloseIcon fontSize="small" />
                </IconButton>
              </Tooltip>

              <Box
                sx={{
                  flexGrow: 1,
                  display: 'flex',
                  flexDirection: 'column',
                  padding: '16px',
                }}
              >
                {/* Title and Description */}
                <Box sx={{ minHeight: '120px' }}>
                  <Typography
                    variant="h6"
                    sx={{ fontWeight: 'bold', marginBottom: '10px', fontSize: '1.2rem', color: '#333' }}
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
                    minHeight: '60px',
                    marginBottom: '15px',
                  }}
                >
                  {course.keySkills.map((skill, index) => (
                    <Chip
                      key={index}
                      label={skill}
                      sx={{
                        backgroundColor: '#e0e0e0',
                        color: '#333',
                        fontWeight: 'bold',
                        fontSize: '0.85rem',
                      }}
                    />
                  ))}
                </Box>

                {/* Progress Bar */}
                <Box sx={{ marginBottom: '15px' }}>
                  <Typography variant="body2" sx={{ marginBottom: '5px', color: '#666' }}>
                    Completion: {course.progress}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={course.progress}
                    sx={{
                      height: '8px',
                      borderRadius: '5px',
                      backgroundColor: '#e0e0e0',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: '#76c7c0',
                      },
                    }}
                  />
                </Box>

                {/* Buttons */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', marginTop: 'auto' }}>
                  <Tooltip title="Chat" arrow>
                    <IconButton
                      sx={{
                        fontSize: '1.5rem',
                        color: '#666',
                      }}
                      onClick={() => openChat(course.id)}
                    >
                      💬
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Prep Plan" arrow>
                    <IconButton
                      sx={{
                        fontSize: '1.5rem',
                        color: '#666',
                      }}
                      onClick={() => openPrepPlan(course.id)}
                    >
                      📝
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>
            </Box>
          </Grid>
        ))}
      </Grid>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={!!courseToDelete}
        onClose={cancelDeleteCourse}
        aria-labelledby="delete-course-dialog-title"
        aria-describedby="delete-course-dialog-description"
      >
        <DialogTitle id="delete-course-dialog-title">Delete Course</DialogTitle>
        <DialogContent>
          <DialogContentText id="delete-course-dialog-description">
            Are you sure you want to delete the course "{courseToDelete?.title}"? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={cancelDeleteCourse} color="primary">
            Cancel
          </Button>
          <Button onClick={confirmDeleteCourse} color="error" autoFocus>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default MockSpacePage;
