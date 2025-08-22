import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function Logo() {
  return <div className="logo">FND</div>;
}

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('http://localhost:5000/predict', { text });
      setResult(response.data);
    } catch (error) {
      console.error('Error:', error);
      setError('Failed to get prediction. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Calculate result color based on prediction
  const getResultColor = () => {
    if (!result || !result.prediction) return '';
    return result.prediction.toLowerCase().includes('fake') ? 'fake-result' : 'real-result';
  };

  return (
    <div className="app-container">
      <header className="header">
        <Logo />
        <h1>Fake News Detector</h1>
      </header>
      <div className="content">
        <form onSubmit={handleSubmit} className="input-form">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter news text here to verify its authenticity..."
            rows="6"
            className="text-input"
          />
          <button type="submit" className="check-button" disabled={loading}>
            {loading ? 'Analyzing...' : 'Check Authenticity'}
          </button>
        </form>
        
        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}
        
        {loading && (
          <div className="loading-indicator">
            <p>Analyzing text...</p>
          </div>
        )}
        
        {result && !loading && (
          <div className={`result-box ${getResultColor()}`}>
            <h2 className="result-heading">Analysis Results</h2>
            <div className="result-item">
              <span className="result-label">Verdict:</span>
              <span className="result-value">{result.prediction}</span>
            </div>
            
            <div className="result-item probability-container">
              <span className="result-label">Confidence:</span>
              <div className="probability-bars">
                <div className="probability-bar">
                  <div className="bar-label">Fake:</div>
                  <div className="bar-container">
                    <div 
                      className="bar fake-bar" 
                      style={{width: `${result.probability[0] * 100}%`}}
                    ></div>
                    <span className="bar-value">{(result.probability[0] * 100).toFixed(1)}%</span>
                  </div>
                </div>
                <div className="probability-bar">
                  <div className="bar-label">Real:</div>
                  <div className="bar-container">
                    <div 
                      className="bar real-bar" 
                      style={{width: `${result.probability[1] * 100}%`}}
                    ></div>
                    <span className="bar-value">{(result.probability[1] * 100).toFixed(1)}%</span>
                  </div>
                </div>
              </div>
            </div>
            
            {result.reasons && result.reasons.length > 0 && (
              <div className="result-item">
                <span className="result-label">Key Indicators:</span>
                <ul className="reasons-list">
                  {result.reasons.map((reason, index) => (
                    <li key={index}>{reason}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {result.similar_real && (
              <div className="result-item">
                <span className="result-label">Similar Real News:</span>
                <p className="similar-news">{result.similar_real}</p>
              </div>
            )}
          </div>
        )}
      </div>
      <footer className="footer">
        <p>© 2023 Fake News Detector | AI-powered news verification</p>
      </footer>
    </div>
  );
}

export default App;