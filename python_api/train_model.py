import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib

# Load datasets with sampling
welfake_df = pd.read_csv('WELFake_Dataset.csv').sample(frac=0.2, random_state=42)
welfake_df = welfake_df[['text', 'label']]
new_df = pd.read_csv('new_dataset.csv').sample(frac=0.2, random_state=42)
liar_df = pd.read_csv('liar_processed.csv').sample(frac=0.2, random_state=42) if 'liar_processed.csv' in os.listdir() else None

# Combine datasets
combined_df = pd.concat([welfake_df, new_df, liar_df] if liar_df is not None else [welfake_df, new_df], ignore_index=True)

# Handle missing values
combined_df = combined_df.dropna(subset=['text', 'label'])

# Prepare features and labels
X = combined_df['text']
y = combined_df['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize text with optimized settings
vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Evaluate
accuracy = model.score(X_test_vec, y_test)
print(f'Accuracy: {accuracy}')

# Save model and vectorizer
joblib.dump(model, 'model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

# Extract top words for explanations
feature_names = vectorizer.get_feature_names_out()
log_prob = model.feature_log_prob_
top_fake_indices = log_prob[0].argsort()[-100:][::-1]
top_real_indices = log_prob[1].argsort()[-100:][::-1]
top_fake_words = [feature_names[i] for i in top_fake_indices]
top_real_words = [feature_names[i] for i in top_real_indices]
joblib.dump(top_fake_words, 'top_fake_words.pkl')
joblib.dump(top_real_words, 'top_real_words.pkl')

# Save real news vectors for similarity search
real_news = combined_df[combined_df['label'] == 1]
real_vectors = vectorizer.transform(real_news['text'])
joblib.dump(real_vectors, 'real_vectors.pkl')
joblib.dump(real_news['text'].tolist(), 'real_texts.pkl')