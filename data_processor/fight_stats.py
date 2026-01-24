import pandas as pd

def finalProcessingForFighter(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["Fighter", "Opp", "Date", "KD", "STR", "TD", "SUB", "Weight_Class", "Winner"]

    fighter_1 = df[[
        "Fighter 1",
        "Fighter 2",
        "Date",
        "Fighter_1_total_KD",
        "Fighter_1_total_STR",
        "Fighter_1_total_TD",
        "Fighter_1_total_SUB",
        "Weight_Class",
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
        "Winner"
    ]].copy()
    fighter_2.columns = cols
    fighter_2["Target"] = (fighter_2["Fighter"] == fighter_2["Winner"]).astype(int)
    fighter_2["Fights"] = 1

    fighters = pd.concat([fighter_1, fighter_2], ignore_index=True)
    
    fighter_stats = (
        fighters.loc[:, ["Fighter", "Date", "Opp", "Weight_Class", "KD", "STR", "TD", "SUB", "Target"]]
        .drop_duplicates(subset=["Fighter", "Date"])
        .rename(columns={
            "KD": "Total_KD",
            "STR": "Total_STR",
            "TD": "Total_TD",
            "SUB": "Total_SUB"
        })
    )
    
    return fighter_stats