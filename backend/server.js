const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();

// Enable CORS for frontend communication with more specific options
app.use(cors({
  origin: ['http://localhost:3000', 'http://127.0.0.1:3000'],
  methods: ['GET', 'POST'],
  credentials: true
}));

// Parse JSON request bodies
app.use(express.json());

// Route to handle prediction requests
app.post('/predict', async (req, res) => {
  const { text } = req.body;
  try {
    const response = await axios.post('http://localhost:5001/predict', { text });
    res.json(response.data);
  } catch (error) {
    console.error('Error calling Python API:', error.message);
    res.status(500).json({ error: 'Error calling Python API' });
  }
});

// Start server on port 5000
app.listen(5000, () => console.log('Server running on port 5000'));