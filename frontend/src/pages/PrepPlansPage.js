import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  List,
  ListItem,
  IconButton,
  Checkbox,
  Collapse,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';

const PrepPlansPage = () => {
  const [modules, setModules] = useState([]);
  const [expanded, setExpanded] = useState({}); // Tracks which modules are expanded

  // Simulate fetching data from a backend
  useEffect(() => {
    const fetchData = async () => {
      const placeholderData = [
        {
          title: 'Understanding Basics',
          description: 'Placeholder summary for Module 1.',
          fullContent: 'Full content for Module 1. Add detailed explanation, links, and checklist here.',
          links: ['https://example.com/module1-link1', 'https://example.com/module1-link2'],
          checklist: ['Complete the introduction slides', 'Review key concepts'],
        },
        {
          title: 'Hands-On Practice',
          description: 'Placeholder summary for Module 2.',
          fullContent: 'Full content for Module 2. Add detailed instructions, links, and checklist here.',
          links: ['https://example.com/module2-link1'],
          checklist: ['Prepare lab materials', 'Schedule practice session'],
        },
        {
          title: 'Group Collaboration',
          description: 'Placeholder summary for Module 3.',
          fullContent: 'Full content for Module 3. Add detailed discussion prompts and activity steps.',
          links: [],
          checklist: ['Form teams', 'Prepare group activity instructions'],
        },
      ];
      setModules(placeholderData);
    };

    fetchData();
  }, []);

  const toggleExpand = (index) => {
    setExpanded((prev) => ({ ...prev, [index]: !prev[index] }));
  };

  const addLink = (index) => {
    const newLink = prompt('Enter the link:');
    if (newLink) {
      const updatedModules = [...modules];
      updatedModules[index].links.push(newLink);
      setModules(updatedModules);
    }
  };

  const addChecklistItem = (index) => {
    const newItem = prompt('Enter the checklist item:');
    if (newItem) {
      const updatedModules = [...modules];
      updatedModules[index].checklist.push(newItem);
      setModules(updatedModules);
    }
  };

  const removeChecklistItem = (moduleIndex, itemIndex) => {
    const updatedModules = [...modules];
    updatedModules[moduleIndex].checklist.splice(itemIndex, 1);
    setModules(updatedModules);
  };

  return (
    <Box
      sx={{
        padding: '20px 50px',
        backgroundColor: '#ffffff',
        height: '90vh',
        overflowY: 'auto',
        position: 'relative',
        scrollbarWidth: 'none',
        '-ms-overflow-style': 'none',
        '&::-webkit-scrollbar': {
          display: 'none',
        },
        paddingBottom: '200px',
        '& > *:last-child': {
          marginBottom: '200px',
        },
      }}
    >
      {/* Modules Section */}
      {modules.map((module, index) => (
        <Card
          key={index}
          sx={{
            backgroundColor: '#ffffff',
            borderRadius: '10px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            marginBottom: '20px',
            border: '1px solid rgba(0,0,0,0.08)',
          }}
        >
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                Module {index + 1}: {module.title}
              </Typography>
              <IconButton onClick={() => toggleExpand(index)}>
                {expanded[index] ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              </IconButton>
            </Box>
            <Typography variant="body2" sx={{ marginY: '10px' }}>
              {module.description}
            </Typography>

            <Collapse in={expanded[index]} timeout="auto" unmountOnExit>
              <Typography variant="body2" sx={{ marginTop: '10px' }}>
                {module.fullContent}
              </Typography>

              {/* Links Section */}
              <Typography variant="subtitle1" sx={{ marginTop: '10px', fontWeight: 'bold' }}>
                Links
              </Typography>
              <List>
                {module.links.map((link, linkIndex) => (
                  <ListItem key={linkIndex} sx={{ padding: '5px 0' }}>
                    <a href={link} target="_blank" rel="noopener noreferrer" style={{ color: '#007bff' }}>
                      {link}
                    </a>
                  </ListItem>
                ))}
              </List>
              <Button
                size="small"
                variant="outlined"
                onClick={() => addLink(index)}
                sx={{ marginTop: '10px', textTransform: 'none' }}
                startIcon={<AddIcon />}
              >
                Add Link
              </Button>

              {/* Checklist Section */}
              <Typography variant="subtitle1" sx={{ marginTop: '20px', fontWeight: 'bold' }}>
                Checklist
              </Typography>
              <List>
                {module.checklist.map((item, itemIndex) => (
                  <ListItem
                    key={itemIndex}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '5px 0',
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                      <Checkbox />
                      <Typography>{item}</Typography>
                    </Box>
                    <IconButton onClick={() => removeChecklistItem(index, itemIndex)}>
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </ListItem>
                ))}
              </List>
              <Button
                size="small"
                variant="outlined"
                onClick={() => addChecklistItem(index)}
                sx={{ marginTop: '10px', textTransform: 'none' }}
                startIcon={<AddIcon />}
              >
                Add Checklist Item
              </Button>
            </Collapse>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default PrepPlansPage;
