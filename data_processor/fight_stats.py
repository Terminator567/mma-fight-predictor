import pandas as pd

def fightStats(df: pd.DataFrame):
    df['KD_diff'] = df['Fighter_1_KD'] - df['Fighter_2_KD']
    df['STR_diff'] = df['Fighter_1_STR'] - df['Fighter_2_STR']
    df['TD_diff'] = df['Fighter_1_TD'] - df['Fighter_2_TD']
    df['SUB_diff'] = df['Fighter_1_SUB'] - df['Fighter_2_SUB']
    
    return df


def fighterDataframe(df: pd.DataFrame):
    df['target'] = (df['Winner'] == df['Fighter 1']).astype(int)
    return df


import pandas as pd

def fighterStats(processed_df: pd.DataFrame) -> pd.DataFrame:
    original_df = pd.read_csv('../data/original.csv')

    cols = ["Name", "KD", "STR", "TD", "SUB", "Winner"]

    fighter_1 = processed_df[[
        "Fighter 1",
        "Fighter_1_KD",
        "Fighter_1_STR",
        "Fighter_1_TD",
        "Fighter_1_SUB",
        "Winner"
    ]].copy()
    fighter_1.columns = cols
    fighter_1["WINS"] = (fighter_1["Name"] == fighter_1["Winner"]).astype(int)
    fighter_1["Fights"] = 1

    fighter_2 = processed_df[[
        "Fighter 2",
        "Fighter_2_KD",
        "Fighter_2_STR",
        "Fighter_2_TD",
        "Fighter_2_SUB",
        "Winner"
    ]].copy()
    fighter_2.columns = cols
    fighter_2["WINS"] = (fighter_2["Name"] == fighter_2["Winner"]).astype(int)
    fighter_2["Fights"] = 1

    fighters = pd.concat([fighter_1, fighter_2], ignore_index=True)

    fighter_stats = fighters.groupby("Name", as_index=False).agg(
        avg_KD=("KD", "mean"),
        avg_STR=("STR", "mean"),
        avg_TD=("TD", "mean"),
        avg_SUB=("SUB", "mean"),
        win_rate=("WINS", "mean")
    )

    original_df = original_df.merge(
        fighter_stats.add_prefix("F1_"),
        left_on="Fighter 1",
        right_on="F1_Name",
        how="left"
    ).drop(columns=["F1_Name"])

    original_df = original_df.merge(
        fighter_stats.add_prefix("F2_"),
        left_on="Fighter 2",
        right_on="F2_Name",
        how="left"
    ).drop(columns=["F2_Name"])

    return original_df


df = pd.read_csv('../data/original.csv')
df = fightStats(df)
df = fighterDataframe(df)
#df = fighterStats(df)
df.to_csv('../data/processed.csv', index=False)