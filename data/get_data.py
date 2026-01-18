from pathlib import Path
from pandas import read_csv, DataFrame

def get_dataframe() -> DataFrame:
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "original.csv"
    return read_csv(csv_path)