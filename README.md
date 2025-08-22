# Fake News Detector - AI-Powered News Verification System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Overview

An intelligent web application that uses machine learning to detect fake news articles in real-time. Built with React frontend, Express.js backend, and Python Flask ML API, this system provides accurate predictions with explanatory insights.

## ✨ Features

- **Real-time Detection**: Instant fake news classification
- **Confidence Scoring**: Probability-based predictions
- **Explainable AI**: Key indicators influencing decisions
- **Similar Content**: Matching with verified real news
- **Responsive Design**: Works on all devices
- **Multi-dataset Training**: Trained on diverse news datasets

## 🛠️ Technology Stack

### Frontend
- **React 18.2.0** - Modern UI framework
- **Axios** - HTTP client for API communication
- **Custom CSS** - Responsive styling

### Backend
- **Express.js 5.1.0** - Web application framework
- **CORS** - Cross-origin resource sharing
- **Node.js** - Runtime environment

### Machine Learning
- **Python Flask 3.0.3** - ML API framework
- **Scikit-learn 1.5.2** - Machine learning library
- **Multinomial Naive Bayes** - Classification algorithm
- **TF-IDF Vectorization** - Text feature extraction
- **NumPy & Pandas** - Data processing

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │  Express.js     │    │   Flask ML      │
│   (Port 3000)   │───▶│   (Port 5000)   │───▶│   (Port 5001)   │
│                 │    │                 │    │                 │
│ • User Interface│    │ • API Gateway   │    │ • ML Processing │
│ • Visualizations│    │ • Request Proxy │    │ • Predictions   │
│ • Form Handling │    │ • CORS Handling │    │ • Explanations  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nihal07g/fake-news-detector-ml.git
cd fake-news-detector-ml
```

2. **Setup Frontend**
```bash
cd frontend
npm install
```

3. **Setup Backend**
```bash
cd backend
npm install
```

4. **Setup Python ML API**
```bash
cd python_api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

5. **Train the Model**
```bash
python train_model.py
```

### Running the Application

Start all three services in separate terminals:

```bash
# Terminal 1: ML API
cd python_api
python app.py

# Terminal 2: Backend
cd backend
npm start

# Terminal 3: Frontend
cd frontend
npm start
```

Visit `http://localhost:3000` in your browser.

## 📊 Model Performance

- **Algorithm**: Multinomial Naive Bayes
- **Features**: 3,000 TF-IDF features with bi-grams
- **Datasets**: WELFake, Custom News, LIAR (optional)
- **Accuracy**: Optimized through cross-validation
- **Response Time**: < 2 seconds

## 🎮 Usage

1. **Enter News Text**: Paste or type news article content
2. **Click Analyze**: Press "Check Authenticity" button
3. **View Results**: See prediction with confidence scores
4. **Understand Decision**: Review key indicators
5. **Compare Content**: View similar real news (if fake detected)

## 📁 Project Structure

```
fake-news-detector-ml/
├── frontend/                 # React application
│   ├── src/
│   │   ├── App.js           # Main component
│   │   ├── App.css          # Styles
│   │   └── index.js         # Entry point
│   ├── public/              # Static assets
│   └── package.json         # Dependencies
├── backend/                 # Express server
│   ├── server.js           # API gateway
│   └── package.json        # Dependencies
├── python_api/             # ML processing
│   ├── app.py              # Flask API
│   ├── train_model.py      # Model training
│   ├── preprocess_*.py     # Data preprocessing
│   ├── requirements.txt    # Python deps
│   └── *.pkl               # Model artifacts
├── .gitignore              # Git ignore rules
└── README.md               # Documentation
```

## 🔧 Configuration

### Environment Variables (Optional)
Create `.env` files for custom configurations:

```env
# Backend (.env)
PORT=5000
PYTHON_API_URL=http://localhost:5001

# Python API (.env)
FLASK_PORT=5001
MODEL_PATH=./model.pkl
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📈 Future Enhancements

- [ ] Deep learning models (BERT, LSTM)
- [ ] Multi-language support
- [ ] User authentication
- [ ] Batch processing
- [ ] Advanced visualizations
- [ ] Mobile application
- [ ] Cloud deployment

## 🐛 Known Issues

- Large dataset files not included in repository
- Model retraining required for optimal performance
- CORS configuration for production deployment

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Nihal** - [GitHub](https://github.com/nihal07g)

## 🙏 Acknowledgments

- WELFake Dataset contributors
- Scikit-learn community
- React development team
- Open source community

---

**⭐ Star this repository if you found it helpful!**