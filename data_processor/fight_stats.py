import pandas as pd
from pathlib import Path

def fightStats(df: pd.DataFrame):
    df['KD_diff'] = df['Fighter_1_KD'] - df['Fighter_2_KD']
    df['STR_diff'] = df['Fighter_1_STR'] - df['Fighter_2_STR']
    df['TD_diff'] = df['Fighter_1_TD'] - df['Fighter_2_TD']
    df['SUB_diff'] = df['Fighter_1_SUB'] - df['Fighter_2_SUB']
    
    return df


def fighterDataframe(df: pd.DataFrame):
    df['target'] = (df['Winner'] == 'Fighter 1').astype(int)
    return df

def fight_stats(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Event Name"] = df["Event Name"].astype(str)

    df["KD_diff"] = df["Fighter_1_KD"] - df["Fighter_2_KD"]
    df["STR_diff"] = df["Fighter_1_STR"] - df["Fighter_2_STR"]
    df["TD_diff"] = df["Fighter_1_TD"] - df["Fighter_2_TD"]
    df["SUB_diff"] = df["Fighter_1_SUB"] - df["Fighter_2_SUB"]

    df["target"] = (df["Winner"] == df["Fighter 1"]).astype(int)

    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR.parent / "data"

    ufc_path = DATA_DIR / "ufc_with_career_stats.csv"
    ufc = pd.read_csv(ufc_path)
    ufc = ufc.copy()
    ufc["Date"] = pd.to_datetime(ufc["Date"], errors="coerce")
    ufc["Event Name"] = ufc["Event Name"].astype(str)

    stat_cols = [
        "Fighter_1_KD","Fighter_2_KD",
        "Fighter_1_STR","Fighter_2_STR",
        "Fighter_1_TD","Fighter_2_TD",
        "Fighter_1_SUB","Fighter_2_SUB",
    ]
    for c in stat_cols:
        ufc[c] = pd.to_numeric(ufc[c], errors="coerce").fillna(0.0)

    ufc = ufc.sort_values(["Date", "Event Name", "Round", "Time"], ascending=[True, True, True, True]).reset_index(drop=True)

    def _mk_key(date_series, event_series, f1_series, f2_series):
        return (
            date_series.astype(str) + "|" +
            event_series.astype(str) + "|" +
            f1_series.astype(str) + "|" +
            f2_series.astype(str)
        )

    ufc["fight_key"] = _mk_key(ufc["Date"], ufc["Event Name"], ufc["Fighter 1"], ufc["Fighter 2"])
    df["fight_key"]  = _mk_key(df["Date"],  df["Event Name"],  df["Fighter 1"],  df["Fighter 2"])

    f1 = pd.DataFrame({
        "fight_key": ufc["fight_key"],
        "fighter": ufc["Fighter 1"],
        "KD": ufc["Fighter_1_KD"],
        "STR": ufc["Fighter_1_STR"],
        "TD": ufc["Fighter_1_TD"],
        "SUB": ufc["Fighter_1_SUB"],
        "win": (ufc["Winner"] == ufc["Fighter 1"]).astype(int),
        "Date": ufc["Date"],
        "Event Name": ufc["Event Name"],
    })
    f2 = pd.DataFrame({
        "fight_key": ufc["fight_key"],
        "fighter": ufc["Fighter 2"],
        "KD": ufc["Fighter_2_KD"],
        "STR": ufc["Fighter_2_STR"],
        "TD": ufc["Fighter_2_TD"],
        "SUB": ufc["Fighter_2_SUB"],
        "win": (ufc["Winner"] == ufc["Fighter 2"]).astype(int),
        "Date": ufc["Date"],
        "Event Name": ufc["Event Name"],
    })

    long_df = pd.concat([f1, f2], ignore_index=True)
    long_df = long_df.sort_values(["fighter", "Date", "Event Name"]).reset_index(drop=True)

    long_df["fights_so_far"] = long_df.groupby("fighter").cumcount()

    for stat in ["KD", "STR", "TD", "SUB", "win"]:
        long_df[f"career_avg_{stat}"] = (
            long_df.groupby("fighter")[stat]
            .expanding()
            .mean()
            .reset_index(level=0, drop=True)
            .shift(1)
        )

    for stat in ["KD", "STR", "TD", "SUB", "win"]:
        long_df[f"last5_avg_{stat}"] = (
            long_df.groupby("fighter")[stat]
            .rolling(window=5, min_periods=1)
            .mean()
            .reset_index(level=0, drop=True)
            .shift(1)
        )

    feat_cols = ["fights_so_far"] + [c for c in long_df.columns if c.startswith("career_avg_") or c.startswith("last5_avg_")]
    long_df[feat_cols] = long_df[feat_cols].fillna(0.0)

    f1_feat = long_df[["fight_key", "fighter"] + feat_cols].rename(columns={"fighter": "Fighter 1"})
    f1_feat = f1_feat.rename(columns={c: f"F1_{c}" for c in feat_cols})
    df = df.merge(f1_feat.drop(columns=["Fighter 1"]), on="fight_key", how="left")

    f2_feat = long_df[["fight_key", "fighter"] + feat_cols].rename(columns={"fighter": "Fighter 2"})
    f2_feat = f2_feat.rename(columns={c: f"F2_{c}" for c in feat_cols})
    df = df.merge(f2_feat.drop(columns=["Fighter 2"]), on="fight_key", how="left")

    new_cols = [c for c in df.columns if c.startswith("F1_") or c.startswith("F2_")]
    df[new_cols] = df[new_cols].fillna(0.0)

    if "F1_career_avg_STR" in df.columns and "F2_career_avg_STR" in df.columns:
        df["career_avg_STR_diff"] = df["F1_career_avg_STR"] - df["F2_career_avg_STR"]

    if "F1_career_avg_win" in df.columns and "F2_career_avg_win" in df.columns:
        df["career_winrate_diff"] = df["F1_career_avg_win"] - df["F2_career_avg_win"]

    if "F1_last5_avg_STR" in df.columns and "F2_last5_avg_STR" in df.columns:
        df["last5_avg_STR_diff"] = df["F1_last5_avg_STR"] - df["F2_last5_avg_STR"]

    if "F1_last5_avg_win" in df.columns and "F2_last5_avg_win" in df.columns:
        df["last5_winrate_diff"] = df["F1_last5_avg_win"] - df["F2_last5_avg_win"]

    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].round(2)

    return df

if __name__ == "__main__":
    import pandas as pd
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent

    DATA_DIR = BASE_DIR.parent / "data"

    processed_path = DATA_DIR / "processed.csv"

    df = pd.read_csv(processed_path)
    df = fight_stats(df)
    df.to_csv(processed_path, index=False)
