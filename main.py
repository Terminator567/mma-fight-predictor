from data_processor.fight_stats import fighterDataframe, fightStats
from data.get_data import get_dataframe
from data_processor.data_types_fixes import check_and_process_data_type

# df = get_dataframe("original.csv")

# # check_and_process_data_type(df)
# df1 = fightStats(df)
# df2 = 
# print(df1.head())

df = get_dataframe("processed.csv")
df1 = fighterDataframe(df)
print(df1.head())

