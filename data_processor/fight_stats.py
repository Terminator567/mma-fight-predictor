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
    return df