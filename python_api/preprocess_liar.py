import pandas as pd

# Load LIAR dataset (train.tsv)
liar_df = pd.read_csv(r'C:\Users\nihal\Downloads\LIAR-PLUS-master\dataset\tsv\train.tsv', sep='\t')

# Map labels to binary (0 for false/pants-fire, 1 for true/mostly-true, etc.)
label_map = {'pants-fire': 0, 'false': 0, 'mostly-false': 0, 'half-true': 1, 'mostly-true': 1, 'true': 1}
liar_df['label'] = liar_df['label'].map(label_map)

# Select text and label
liar_processed = liar_df[['statement', 'label']].rename(columns={'statement': 'text'})

# Handle missing values
liar_processed = liar_processed.dropna(subset=['text', 'label'])

# Save to CSV
liar_processed.to_csv('liar_processed.csv', index=False)

# Print confirmation
print(f"Processed {len(liar_processed)} entries and saved to liar_processed.csv")