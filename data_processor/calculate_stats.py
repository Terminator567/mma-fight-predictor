import pandas as pd

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    df['Fighter_1_total_SUB'] = 0
    df['Fighter_2_total_SUB'] = 0
    df['Fighter_1_total_KD'] = 0
    df['Fighter_2_total_KD'] = 0
    df['Fighter_1_total_STR'] = 0
    df['Fighter_2_total_STR'] = 0
    df['Fighter_1_total_TD'] = 0
    df['Fighter_2_total_TD'] = 0
    fighter_stats = {}
    
    for idx, row in df.iterrows():
        f1 = row['Fighter 1']
        f2 = row['Fighter 2']
        
        if f1 not in fighter_stats:
            fighter_stats[f1] = {'SUB': 0, 'KD': 0, 'STR': 0, 'TD': 0}
        if f2 not in fighter_stats:
            fighter_stats[f2] = {'SUB': 0, 'KD': 0, 'STR': 0, 'TD': 0}
 
        df.at[idx, 'Fighter_1_total_SUB'] = fighter_stats[f1]['SUB']
        df.at[idx, 'Fighter_2_total_SUB'] = fighter_stats[f2]['SUB']
        df.at[idx, 'Fighter_1_total_KD'] = fighter_stats[f1]['KD']
        df.at[idx, 'Fighter_2_total_KD'] = fighter_stats[f2]['KD']
        df.at[idx, 'Fighter_1_total_STR'] = fighter_stats[f1]['STR']
        df.at[idx, 'Fighter_2_total_STR'] = fighter_stats[f2]['STR']
        df.at[idx, 'Fighter_1_total_TD'] = fighter_stats[f1]['TD']
        df.at[idx, 'Fighter_2_total_TD'] = fighter_stats[f2]['TD']

        fighter_stats[f1]['SUB'] += row['Fighter_1_SUB']
        fighter_stats[f2]['SUB'] += row['Fighter_2_SUB']
        fighter_stats[f1]['KD'] += row['Fighter_1_KD']
        fighter_stats[f2]['KD'] += row['Fighter_2_KD']
        fighter_stats[f1]['STR'] += row['Fighter_1_STR']
        fighter_stats[f2]['STR'] += row['Fighter_2_STR']
        fighter_stats[f1]['TD'] += row['Fighter_1_TD']
        fighter_stats[f2]['TD'] += row['Fighter_2_TD']
    
    return df

df = pd.read_csv('../data/original.csv')
df = calculate_statistics(df)
df.to_csv('../data/ufc_with_career_stats.csv', index=False)
