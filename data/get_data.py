from pathlib import Path
from pandas import read_csv, DataFrame

def get_dataframe(file: str) -> DataFrame:
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / file
    return read_csv(csv_path)

def convert_to_csv(df: DataFrame):
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "processed.csv"
    df.to_csv(csv_path, index=False)