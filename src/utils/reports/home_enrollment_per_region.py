import dash
from dash import dcc, html

from numpy import average
import plotly.express as px
import pandas as pd


# -- Create the appropriate plot
df1 = pd.read_csv("database/processed/enrollment.csv")
df2 = pd.read_csv("database/processed/ES_JHS_enroll.csv")
df3 = pd.read_csv("database/processed/SHS_enroll.csv")

es_df = df1.merge(df2, on='enroll_id')
shs_df = df1.merge(df3, on='enroll_id')
dataframe = pd.concat([es_df, shs_df])

query = dataframe.groupby('grade', as_index=False)[['counts']].sum()


# Ploting
home_enrollment_per_region = px.bar(query, x="grade", y="counts")
home_enrollment_per_region

# Layout configs
home_enrollment_per_region.update_layout(
    autosize=True,
    margin={"l": 16, "r": 16, "t": 16, "b": 16},  # Optional: Adjust margins
)



## -- INDICATORS: Total Enrollees
def format_large_number(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)

es_count = es_df['counts'].sum()
shs_count = shs_df['counts'].sum()

total_enrollees = format_large_number(es_count + shs_count)
total_enrollees



## -- INDICATORS: Most and Least active school level
most_active =   query.loc[query['counts'].idxmax()]
least_active =  query.loc[query['counts'].idxmin()]



## -- INDICATORS: Total Enrollees
count_shs_school = shs_df['beis_id'].nunique()
total_shs_enrollees = shs_df['counts'].sum()
total_shs_enrollees


# Ratio per Strand
total_enrollees_per_strand = shs_df.groupby('strand', as_index=False)['counts'].sum()
total_enrollees_per_strand['ratio'] = total_enrollees_per_strand['counts'] / total_shs_enrollees
total_enrollees_per_strand

academic_track_ratio = total_enrollees_per_strand[total_enrollees_per_strand['strand'] == 'ACAD'].values.tolist()[0][2]

# Ratio per track
total_enrollees_per_track = shs_df[
                                shs_df['strand'] == 'ACAD'
                            ].groupby('track', as_index=False)['counts'].sum()
total_enrollees_per_track['ratio'] = total_enrollees_per_track['counts'] / total_shs_enrollees
total_enrollees_per_track

filtered_non_acad = total_enrollees_per_strand[total_enrollees_per_strand['strand'] == 'NON ACAD'].values.tolist()[0]
total_enrollees_per_track.loc[len(total_enrollees_per_track)] = pd.Series(filtered_non_acad, index=total_enrollees_per_track.columns)
total_enrollees_per_track


# avg_stem = shs_df[shs_df['track'] == 'STEM']['counts'].sum() / total_shs_enrollees
# avg_stem

# average_per_track = shs_df['track'].value_counts(normalize=True)
# average_per_track

# Ploting
track_ratio_per_track = px.pie(total_enrollees_per_strand, names="strand", values="ratio")
track_ratio_per_track

# Layout configs
track_ratio_per_track.update_layout(
    autosize=True,
    margin={"l": 16, "r": 16, "t": 16, "b": 16},  # Optional: Adjust margins
)
