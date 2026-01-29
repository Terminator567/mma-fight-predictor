from pandas import DataFrame
import pandas as pd

def categories_columns(df: DataFrame):
    df = df.copy()
    
    col_to_codes = ["Fighter", "Opp", "Weight_Class"]
    
    for col in col_to_codes:
        try:
            df[f"{col}_code"] = df[col].astype("category").cat.codes
        except:
            pass
    
    return df
