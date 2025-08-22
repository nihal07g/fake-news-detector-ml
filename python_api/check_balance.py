import pandas as pd

# Load the combined dataset
welfake_df = pd.read_csv('WELFake_Dataset.csv')
new_df = pd.read_csv('new_dataset.csv')
combined_df = pd.concat([welfake_df, new_df], ignore_index=True)
combined_df = combined_df[['text', 'label']]

# Check label distribution
label_counts = combined_df['label'].value_counts()
print(label_counts)

# Calculate percentages
total = len(combined_df)
fake_percentage = (label_counts[0] / total) * 100
real_percentage = (label_counts[1] / total) * 100
print(f"Fake: {fake_percentage:.2f}%")
print(f"Real: {real_percentage:.2f}%")