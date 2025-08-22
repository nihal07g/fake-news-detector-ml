import pandas as pd

# Paths to the new dataset files
fake_path = r'C:\Users\nihal\Downloads\Fake.csv'
true_path = r'C:\Users\nihal\Downloads\True.csv'

# Load fake news
fake_df = pd.read_csv(fake_path)
fake_df['label'] = 0  # Fake

# Load true news
true_df = pd.read_csv(true_path)
true_df['label'] = 1  # Real

# Concatenate
new_df = pd.concat([fake_df, true_df], ignore_index=True)

# Select only 'text' and 'label'
new_df = new_df[['text', 'label']]

# Handle missing values
new_df = new_df.dropna(subset=['text', 'label'])

# Save to a new CSV for combination
new_df.to_csv('new_dataset.csv', index=False)