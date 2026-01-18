import pandas as pd

data = pd.read_csv('/Users/sheelavprakash/Desktop/mma-fight-predictor/data/ufc export 2026-01-17 09-44-36.csv')
print("First 5 fights:")
print(data.head())

print("\n")
print(f"Total fights: {len(data)}")

print("\n")
print("Columns:")
print(data.columns.tolist())

print("\n")
print("Who wins more?")
print(data['Winner'].value_counts())
