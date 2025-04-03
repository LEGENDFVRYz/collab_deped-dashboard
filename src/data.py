import pandas as pd


# Data Process
df1 = pd.read_csv("database/processed/enrollment.csv")
df2 = pd.read_csv("database/processed/ES_JHS_enroll.csv")
df3 = pd.read_csv("database/processed/SHS_enroll.csv")

es_df = df1.merge(df2, on='enroll_id', how='left')
shs_df = df1.merge(df3, on='enroll_id', how='left')
dataframe = pd.concat([es_df, shs_df])
