from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import logging
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})

# Model loading with safety checks
def load_model_safely(filepath, description):
    """Load model artifacts with error handling"""
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{description} not found at {filepath}")
        
        model_data = joblib.load(filepath)
        logger.info(f"Successfully loaded {description}")
        return model_data
    except Exception as e:
        logger.error(f"Failed to load {description}: {str(e)}")
        raise

def validate_model_integrity():
    """Validate that all required model components are functional"""
    try:
        # Test basic model functionality
        test_text = ["This is a test news article about politics."]
        test_vec = vectorizer.transform(test_text)
        
        # Check prediction capability
        prediction = model.predict(test_vec)
        probability = model.predict_proba(test_vec)
        
        # Validate prediction format
        assert len(prediction) == 1, "Model should return single prediction"
        assert len(probability[0]) == 2, "Model should return binary probabilities"
        assert 0 <= prediction[0] <= 1, "Prediction should be 0 or 1"
        
        # Test nearest neighbors
        if len(real_vectors) > 0:
            nn.kneighbors(test_vec, n_neighbors=1)
        
        logger.info("Model validation passed successfully")
        return True
    except Exception as e:
        logger.error(f"Model validation failed: {str(e)}")
        return False

# Load model and resources with error handling
try:
    logger.info("Starting model loading process...")
    
    model = load_model_safely('model.pkl', 'ML classification model')
    vectorizer = load_model_safely('vectorizer.pkl', 'TF-IDF vectorizer')
    top_fake_words = load_model_safely('top_fake_words.pkl', 'fake words indicators')
    top_real_words = load_model_safely('top_real_words.pkl', 'real words indicators')
    real_vectors = load_model_safely('real_vectors.pkl', 'real news vectors')
    real_texts = load_model_safely('real_texts.pkl', 'real news texts')
    
    # Initialize nearest neighbors
    nn = NearestNeighbors(n_neighbors=1, metric='cosine')
    nn.fit(real_vectors)
    
    # Validate model integrity
    if not validate_model_integrity():
        raise Exception("Model validation failed")
        
    logger.info("All models loaded and validated successfully")
    
except Exception as e:
    logger.critical(f"Failed to initialize ML models: {str(e)}")
    logger.critical("Application cannot start without proper models")
    exit(1)

# Enhanced reasoning function with error handling
def get_reasons(text, prediction):
    """Generate explanations for predictions with error handling"""
    try:
        text_vec = vectorizer.transform([text]).toarray()[0]
        feature_names = vectorizer.get_feature_names_out()
        log_prob = model.feature_log_prob_
        
        present_indices = [i for i, val in enumerate(text_vec) if val > 0]
        
        if not present_indices:
            return ["No recognizable features found"]
        
        word_contributions = [
            (feature_names[i], log_prob[prediction][i] * text_vec[i]) 
            for i in present_indices
        ]
        
        word_contributions.sort(key=lambda x: abs(x[1]), reverse=True)
        top_n = min(3, len(word_contributions))
        top_words = [word for word, _ in word_contributions[:top_n]]
        
        return top_words if top_words else ["No specific indicators identified"]
    
    except Exception as e:
        logger.error(f"Error generating reasons: {str(e)}")
        return ["Unable to generate explanation"]

# Prediction endpoint with enhanced error handling
@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint with comprehensive error handling"""
    try:
        # Request validation
        if not request.json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.json
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text field is required and cannot be empty'}), 400
        
        if len(text) > 50000:
            return jsonify({'error': 'Text too long (max 50,000 characters)'}), 400
        
        # Log prediction request (without sensitive data)
        logger.info(f"Processing prediction request - text length: {len(text)} chars")
        
        # Vectorize input text
        try:
            text_vec = vectorizer.transform([text])
        except Exception as e:
            logger.error(f"Vectorization failed: {str(e)}")
            return jsonify({'error': 'Failed to process text format'}), 400
        
        # Get prediction and probability
        try:
            prediction = model.predict(text_vec)[0]
            probability = model.predict_proba(text_vec)[0]
        except Exception as e:
            logger.error(f"Model prediction failed: {str(e)}")
            return jsonify({'error': 'Model prediction failed'}), 500
        
        # Generate explanations
        reasons = get_reasons(text, prediction)
        
        # Build response
        response = {
            'prediction': 'fake' if prediction == 0 else 'real',
            'probability': probability.tolist(),
            'reasons': reasons
        }
        
        # Add similar real news for fake predictions
        if prediction == 0:
            try:
                dist, idx = nn.kneighbors(text_vec, n_neighbors=1)
                if len(real_texts) > idx[0][0]:
                    similar_real = real_texts[idx[0][0]]
                    response['similar_real'] = similar_real
            except Exception as e:
                logger.warning(f"Failed to find similar real news: {str(e)}")
                # Continue without similar news rather than failing
        
        logger.info(f"Prediction completed: {response['prediction']} "
                   f"(confidence: {max(probability):.2f})")
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Unexpected error in predict endpoint: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Quick model validation
        test_vec = vectorizer.transform(["test"])
        model.predict(test_vec)
        
        return jsonify({
            'status': 'healthy',
            'service': 'fake-news-ml-api',
            'version': '1.0.0',
            'models_loaded': True
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Flask ML API server...")
    app.run(host='0.0.0.0', port=5001, debug=False)