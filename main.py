from data_processor.fight_stats import fighterStats
from data.get_data import get_dataframe, convert_to_csv
from data_processor.data_types_fixes import check_and_process_data_type
from data_processor.data_cleaner import clean_data
from data_processor.calculate_stats import calculate_statistics

df = get_dataframe("processed.csv")

df = check_and_process_data_type(df)

df = clean_data(df)
df = calculate_statistics(df)

# df = fighterStats(df)

print(df)

