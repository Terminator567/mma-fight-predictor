from pandas import DataFrame, to_datetime, to_timedelta

def check_and_process_data_type(df: DataFrame):
    df = df.copy()
    
    columns_to_float = [
        "Fighter_1_KD", "Fighter_2_KD",
        "Fighter_1_STR", "Fighter_2_STR",
        "Fighter_1_TD", "Fighter_2_TD",
        "Fighter_1_SUB", "Fighter_2_SUB", 
        "Round", "Time"
    ]
    
    if "Date" in df.columns:
        df['Date'] = to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S.%f")
    
    if "Time" in df.columns:
        df["Time"] = (to_timedelta("00:" + df["Time"])
                            .dt.total_seconds()
                            .astype("Int64"))
    
    existing_columns = [col for col in columns_to_float if col in df.columns]
    df[existing_columns] = df[existing_columns].astype(float)
    
    return df

def drop_col_for_training(df: DataFrame) -> DataFrame:
    df = df.drop('Fighter', axis=1)
    df = df.drop('Date', axis=1)
    df = df.drop('Opp', axis=1)
    df = df.drop('Weight_Class', axis=1)
    df = df.drop('Round', axis=1)
    df = df.drop('Time', axis=1)
    df = df.drop('Fighter_code', axis=1)
    df = df.drop('Opp_code', axis=1)

    return df