import pandas as pd

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    # print("BEFORE CLEANING")
    # print("\n")
    # print(f"Total fights: {len(data)}")
    # print("\n")
    # print("Missing values per column:")
    # print(data.isnull().sum())

    original_count = len(data)
    data = data.dropna(subset=['Winner'])
    data = data.dropna()
    removed_count = original_count - len(data)

    # print(f"Removed {removed_count} fights with missing data")
    # print("\n")
    # print("AFTER CLEANING")
    # print("\n")
    # print(f"Total fights: {len(data)}")
    # print("\n")
    # print("Missing values per column:")
    # print(data.isnull().sum())

    return data