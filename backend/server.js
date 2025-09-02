const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();

// Enhanced CORS configuration for production security
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? ['https://yourdomain.com'] 
    : ['http://localhost:3000', 'http://127.0.0.1:3000'],
  methods: ['GET', 'POST'],
  credentials: true,
  optionsSuccessStatus: 200
}));

// Parse JSON request bodies with size limits
app.use(express.json({ limit: '10mb' }));

// Request validation middleware
const validatePredictRequest = (req, res, next) => {
  const { text } = req.body;
  
  if (!text) {
    return res.status(400).json({ 
      error: 'Text field is required',
      code: 'MISSING_TEXT_FIELD'
    });
  }
  
  if (typeof text !== 'string') {
    return res.status(400).json({ 
      error: 'Text must be a string',
      code: 'INVALID_TEXT_TYPE'
    });
  }
  
  if (text.trim().length === 0) {
    return res.status(400).json({ 
      error: 'Text cannot be empty',
      code: 'EMPTY_TEXT'
    });
  }
  
  if (text.length > 50000) {
    return res.status(400).json({ 
      error: 'Text too long. Maximum 50,000 characters allowed',
      code: 'TEXT_TOO_LONG'
    });
  }
  
  next();
};

// Route to handle prediction requests with enhanced error handling
app.post('/predict', validatePredictRequest, async (req, res) => {
  const { text } = req.body;
  
  try {
    // Set timeout for Python API calls (30 seconds)
    const response = await axios.post('http://localhost:5001/predict', 
      { text }, 
      { 
        timeout: 30000,
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    
    res.json(response.data);
  } catch (error) {
    console.error('Error calling Python API:', error.message);
    
    // Handle different types of errors
    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({ 
        error: 'ML service is unavailable. Please try again later.',
        code: 'SERVICE_UNAVAILABLE'
      });
    }
    
    if (error.code === 'ENOTFOUND') {
      return res.status(503).json({ 
        error: 'Unable to connect to ML service',
        code: 'CONNECTION_ERROR'
      });
    }
    
    if (error.code === 'ETIMEDOUT' || error.message.includes('timeout')) {
      return res.status(504).json({ 
        error: 'Request timeout. The text may be too complex to analyze.',
        code: 'REQUEST_TIMEOUT'
      });
    }
    
    if (error.response && error.response.status) {
      return res.status(error.response.status).json({ 
        error: error.response.data?.error || 'Error from ML service',
        code: 'ML_SERVICE_ERROR'
      });
    }
    
    // Generic server error
    res.status(500).json({ 
      error: 'Internal server error. Please try again later.',
      code: 'INTERNAL_ERROR'
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    service: 'fake-news-detector-api'
  });
});

// Global error handler
app.use((error, req, res, next) => {
  console.error('Unhandled error:', error);
  res.status(500).json({ 
    error: 'An unexpected error occurred',
    code: 'UNEXPECTED_ERROR'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ 
    error: 'Endpoint not found',
    code: 'NOT_FOUND'
  });
});

const PORT = process.env.PORT || 5000;

// Start server with error handling
app.listen(PORT, (err) => {
  if (err) {
    console.error('Failed to start server:', err);
    process.exit(1);
  }
  console.log(`Server running on port ${PORT}`);
});