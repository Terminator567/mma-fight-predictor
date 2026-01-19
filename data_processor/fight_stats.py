import pandas as pd

from data.get_data import convert_to_csv

def fightStats(df: pd.DataFrame):
    df['KD_diff'] = df['Fighter_1_KD'] - df['Fighter_2_KD']
    df['STR_diff'] = df['Fighter_1_STR'] - df['Fighter_2_STR']
    df['TD_diff'] = df['Fighter_1_TD'] - df['Fighter_2_TD']
    df['SUB_diff'] = df['Fighter_1_SUB'] - df['Fighter_2_SUB']
    
    convert_to_csv(df)
    
    return df


def fighterDataframe(df: pd.DataFrame):
    df['target'] = (df['Winner'] == 'Fighter 1').astype(int)
    convert_to_csv(df)
    return df


def fighterStats(df: pd.DataFrame):
    
    cols = ["Name", "KD", "STR", "TD", "SUB", "Winner"]
    
    fighter_1 = df[[
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
    
    fighter_2 = df[[
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
    
    
    fighters = pd.concat([fighter_1, fighter_2], ignore_index=False)
    
    
    fighter_stats = fighters.groupby("Name").agg(
        total_KD=("KD", "sum"),
        total_STR=("STR", "sum"),
        total_TD=("TD", "sum"),
        total_SUB=("SUB", "sum"),
        total_wins=("WINS", "sum"),
        total_fights=("Fights", "sum")
    )
    
    fighter_stats["win_rate"] = fighter_stats["total_wins"] / fighter_stats["total_fights"]
    fighter_stats["avg_KD"] = fighter_stats["total_KD"] / fighter_stats["total_fights"]
    fighter_stats["avg_STR"] = fighter_stats["total_STR"] / fighter_stats["total_fights"]
    fighter_stats["avg_TD"] = fighter_stats["total_TD"] / fighter_stats["total_fights"]
    fighter_stats["avg_SUB"] = fighter_stats["total_SUB"] / fighter_stats["total_fights"]
    fighter_stats["offense_score"] = (
        fighter_stats["avg_STR"] + fighter_stats["avg_TD"] + fighter_stats["avg_KD"]
    )
    
    return fighter_stats