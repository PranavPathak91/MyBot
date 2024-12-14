import React, { useState, useRef, useEffect } from 'react';
import { Box, TextField, IconButton, Typography } from '@mui/material';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import SendIcon from '@mui/icons-material/Send';
import BubbleBar from '../components/BubbleBar';

const ChatPage = () => {
  const [messages, setMessages] = useState([]); // Stores the chat messages
  const [input, setInput] = useState(''); // Stores the current input text
  const [showBubbleBar, setShowBubbleBar] = useState(true); // Controls BubbleBar visibility
  const chatBodyRef = useRef(null); // Reference for scrolling to the bottom
  const inputRef = useRef(null); // Reference for input field

  // Auto-scroll to the bottom when messages change
  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages]);

  // Handle sending a message
  const handleSendMessage = () => {
    if (input.trim()) {
      // Hide BubbleBar on first message
      if (showBubbleBar) {
        setShowBubbleBar(false);
      }

      // Add user's message to the message list
      setMessages([...messages, { sender: 'user', text: input }]);
      setInput(''); // Clear the input field

      // Simulate bot response
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          { sender: 'bot', text: 'This is a simulated response from the bot.' },
        ]);
      }, 1000);
    }
  };

  // Handle key press (specifically Enter key)
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <Box 
      data-component="chat-page-root-container"
      sx={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        padding: '10px',
        backgroundColor: '#ffffff',
        overflow: 'hidden',
      }}
    >
      <Box 
        data-component="chat-messages-container"
        ref={chatBodyRef}
        sx={{
          flex: 1,
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          gap: '10px',
          padding: '10px',
          backgroundColor: '#ffffff',
          overflowY: 'auto',
          overflowX: 'hidden',
          position: 'relative',
        }}
      >
        {messages.length === 0 ? (
          <Box 
            data-component="chat-empty-state"
            sx={{
              textAlign: 'center',
              color: '#aaa',
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
            }}
          >
            <Typography>Start a conversation...</Typography>
          </Box>
        ) : (
          messages.map((message, index) => (
            <Box
              data-component="chat-message"
              key={index}
              sx={{
                alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start',
                backgroundColor: message.sender === 'user' ? '#f1f1f1' : '#ffffff',
                padding: '10px 15px',
                borderRadius: '20px',
                maxWidth: '70%',
                wordWrap: 'break-word',
              }}
            >
              {message.text}
            </Box>
          ))
        )}
      </Box>

      {/* BubbleBar now placed just above input container */}
      {showBubbleBar && (
        <Box 
          data-component="bubble-bar-wrapper"
          sx={{
            width: '100%',
            marginBottom: '10px',
          }}
        >
          <BubbleBar />
        </Box>
      )}

      <Box 
        data-component="chat-input-container"
        sx={{
          width: '100%',
          display: 'flex',
          alignItems: 'center',
          padding: '10px',
          backgroundColor: '#ffffff',
          borderRadius: '8px',
          marginTop: '10px',
        }}
      >
        <Box data-component="chat-attachment-icon">
          <IconButton>
            <AttachFileIcon />
          </IconButton>
        </Box>

        <TextField
          data-component="chat-text-input"
          ref={inputRef}
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          sx={{
            marginX: '0px',
            borderRadius: '20px',
            backgroundColor: '#f9f9f9',
            '& .MuiOutlinedInput-root': {
              '& fieldset': {
                border: 'none',
              },
              '&:hover fieldset': {
                border: 'none',
              },
              '&.Mui-focused fieldset': {
                border: 'none',
              },
            },
          }}
        />

        <Box data-component="chat-send-icon">
          <IconButton 
            onClick={handleSendMessage}
            sx={{
              color: input.trim() ? 'black' : 'gray'
            }}
            disabled={!input.trim()}
          >
            <SendIcon />
          </IconButton>
        </Box>
      </Box>
    </Box>
  );
};

export default ChatPage;
