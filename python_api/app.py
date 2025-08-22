from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})

# Load model and resources
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
top_fake_words = joblib.load('top_fake_words.pkl')
top_real_words = joblib.load('top_real_words.pkl')
real_vectors = joblib.load('real_vectors.pkl')
real_texts = joblib.load('real_texts.pkl')

# Initialize nearest neighbors
nn = NearestNeighbors(n_neighbors=1, metric='cosine')
nn.fit(real_vectors)

# Enhanced reasoning function
def get_reasons(text, prediction):
    text_vec = vectorizer.transform([text]).toarray()[0]
    feature_names = vectorizer.get_feature_names_out()
    log_prob = model.feature_log_prob_
    present_indices = [i for i, val in enumerate(text_vec) if val > 0]
    word_contributions = [(feature_names[i], log_prob[prediction][i] * text_vec[i]) for i in present_indices]
    word_contributions.sort(key=lambda x: abs(x[1]), reverse=True)
    top_n = 3
    top_words = [word for word, _ in word_contributions[:top_n]]
    return top_words if top_words else ["No specific reasons identified"]

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data['text']
    
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0]
    
    reasons = get_reasons(text, prediction)
    
    response = {
        'prediction': 'fake' if prediction == 0 else 'real',
        'probability': probability.tolist(),
        'reasons': reasons
    }
    
    if prediction == 0:
        dist, idx = nn.kneighbors(text_vec, n_neighbors=1)
        similar_real = real_texts[idx[0][0]]
        response['similar_real'] = similar_real
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5001)