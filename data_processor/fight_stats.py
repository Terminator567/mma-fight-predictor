import pandas as pd

def fightStats(df: pd.DataFrame):
    df['KD_diff'] = df['Fighter_1_KD'] - df['Fighter_2_KD']
    df['STR_diff'] = df['Fighter_1_STR'] - df['Fighter_2_STR']
    df['TD_diff'] = df['Fighter_1_TD'] - df['Fighter_2_TD']
    df['SUB_diff'] = df['Fighter_1_SUB'] - df['Fighter_2_SUB']
    
    df.to_csv("data/ufc_fight_stats.csv", index=False)
