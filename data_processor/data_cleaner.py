import pandas as pd

data = pd.read_csv('/Users/sheelavprakash/Desktop/mma-fight-predictor/data/original.csv')

print("BEFORE CLEANING")
print("\n")
print(f"Total fights: {len(data)}")
print("\n")
print("Missing values per column:")
print(data.isnull().sum())

original_count = len(data)
data = data.dropna(subset=['Winner'])
data = data.dropna(subset=['Fighter_1_KD', 'Fighter_2_KD', 'Fighter_1_STR', 
                            'Fighter_2_STR', 'Fighter_1_TD', 'Fighter_2_TD', 
                            'Fighter_1_SUB', 'Fighter_2_SUB'])
removed_count = original_count - len(data)

print(f"Removed {removed_count} fights with missing data")
print("\n")
print("AFTER CLEANING")
print("\n")
print(f"Total fights: {len(data)}")
print("\n")
print("Missing values per column:")
print(data.isnull().sum())

data.to_csv('/Users/sheelavprakash/Desktop/mma-fight-predictor/data/ufc_cleaned.csv', index=False)
print("\n")
print("Saved to ufc_cleaned.csv")