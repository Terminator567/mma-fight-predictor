from pandas import DataFrame

def categories_columns(df: DataFrame):
    df = df.copy()
    
    col_to_codes = ["Fighter 1", "Fighter 2" ,"Weight_Class", "Method", "Winner"]
    
    for col in col_to_codes:
        df[f"{col}_code"] = df[col].astype("category").cat.codes
    
    return df