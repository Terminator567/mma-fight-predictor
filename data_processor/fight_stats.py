import pandas as pd

def calculateAverages(df: pd.DataFrame) -> pd.DataFrame:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(['Fighter', 'Date'])

    # Penalize losses
    df['Adj_Time'] = df['Time']
    df.loc[df['Target'] == 0, 'Adj_Time'] = df['Time'] * 2

    df['Adj_Round'] = df['Round']
    df.loc[df['Target'] == 0, 'Adj_Round'] = df['Round'] * 2

    # Historical averages (no leakage)
    df['Avg_Round_Time'] = (
        df.groupby('Fighter')['Adj_Time']
        .transform(lambda s: s.shift().expanding().mean())
    )

    df['Avg_Round'] = (
        df.groupby('Fighter')['Adj_Round']
        .transform(lambda s: s.shift().expanding().mean())
    )
    
    df['Avg_Round_Time'] = df['Avg_Round_Time'].fillna(0)
    df['Avg_Round'] = df['Avg_Round'].fillna(0)
    
    
    df = df.drop('Adj_Time', axis=1)
    df = df.drop('Adj_Round', axis=1)
    
    return df

def finalProcessingForFighter(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["Fighter", "Opp", "Date", "KD", "STR", "TD", "SUB", "Weight_Class", "Round", "Time", "Winner"]

    fighter_1 = df[[
        "Fighter 1",
        "Fighter 2",
        "Date",
        "Fighter_1_total_KD",
        "Fighter_1_total_STR",
        "Fighter_1_total_TD",
        "Fighter_1_total_SUB",
        "Weight_Class",
        "Round",
        "Time",
        "Winner"
    ]].copy()
    fighter_1.columns = cols
    fighter_1["Target"] = (fighter_1["Fighter"] == fighter_1["Winner"]).astype(int)
    fighter_1["Fights"] = 1

    fighter_2 = df[[
        "Fighter 2",
        "Fighter 1",
        "Date",
        "Fighter_1_total_KD",
        "Fighter_1_total_STR",
        "Fighter_1_total_TD",
        "Fighter_1_total_SUB",
        "Weight_Class",
        "Round",
        "Time",
        "Winner"
    ]].copy()
    fighter_2.columns = cols
    fighter_2["Target"] = (fighter_2["Fighter"] == fighter_2["Winner"]).astype(int)
    fighter_2["Fights"] = 1

    fighters = pd.concat([fighter_1, fighter_2], ignore_index=True)
    
    fighter_stats = (
        fighters.loc[:, ["Fighter", "Date", "Opp", "Weight_Class", "KD", "STR", "TD", "SUB", "Round", "Time", "Target"]]
        .drop_duplicates(subset=["Fighter", "Date"])
        .rename(columns={
            "KD": "Total_KD",
            "STR": "Total_STR",
            "TD": "Total_TD",
            "SUB": "Total_SUB"
        })
    )
    
    return fighter_stats