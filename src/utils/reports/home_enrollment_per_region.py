from re import X
import dash
from dash import dcc, html

from numpy import average
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# -- Create the appropriate plot
df1 = pd.read_csv("database/processed/enrollment.csv")
df2 = pd.read_csv("database/processed/ES_JHS_enroll.csv")
df3 = pd.read_csv("database/processed/SHS_enroll.csv")

es_df = df1.merge(df2, on='enroll_id')
shs_df = df1.merge(df3, on='enroll_id')
dataframe = pd.concat([es_df, shs_df])

order = [
    'K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'JHS', 'G11', 'G12'
]

dataframe['school-level'] = dataframe['grade'].apply(
    lambda x: 'JHS' if x in ['G7', 'G8', 'G9', 'G10', 'JHS'] else ('SHS' if x in ['G11', 'G12'] else 'ELEM')
)
dataframe

query = dataframe.groupby(['school-level','grade'], as_index=False)[['counts']].sum()
# print(dataframe.columns)

# Ploting
home_enrollment_per_region = px.bar(query, 
                                    x="counts", 
                                    y="grade",
                                    text=None,
                                    orientation='h',
                                    color='school-level',
                                    color_discrete_map={
                                        'ELEM': '#68d87b', 
                                        'JHS': '#40ad62', 
                                        'SHS': '#138954'    
                                    }
                            )
home_enrollment_per_region

# Layout configs
home_enrollment_per_region.update_layout(yaxis=dict(visible=False), xaxis=dict(visible=False))
home_enrollment_per_region.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 16, "b": 8},  # Optional: Adjust margins
    paper_bgcolor='rgba(0, 0, 0, 0)', 
    plot_bgcolor='rgba(0, 0, 0, 0)',   
    yaxis=dict(showticklabels=False),
    xaxis=dict(
        categoryorder='array',
        categoryarray=order,
    ),
    legend=dict(
        orientation="h",  # Horizontal legend
        yanchor="bottom",  # Align legend at the bottom
        y=-0.2,  # Position it below the chart
        xanchor="center",  # Center it horizontally
        x=0.5  # Align it to the center
    )
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
custom_colors = ['#00AD7F', '#E0E0E0']
explode = [0, 0.15]

track_ratio_per_track = go.Figure(
    data=[
        go.Pie(labels=total_enrollees_per_strand['strand'], 
               values=total_enrollees_per_strand['ratio'], 
               marker=dict(colors=custom_colors),
               pull=explode
    )]
)

# Layout configs
track_ratio_per_track.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 16, "b": 0},  # Optional: Adjust margins
)

# ----------------------------------------------------------
# School Distribution Across Sectors
df4 = pd.read_csv("database/processed/sch_info.csv")
grouped_by_sectors = df4.groupby("sector")
sector_counts = grouped_by_sectors.size().reset_index(name="count")

sector_counts

home_school_number_per_sector = px.bar(sector_counts, x="sector", y="count",
            #  title="Distribution of Schools Across Sectors",
             text="count",
             orientation="v",
             color="sector",
             color_discrete_map={
                'Private': '#68d87b', 
                'Public': '#40ad62', 
                'SUCsLUCs': '#138954'    
             })

home_school_number_per_sector

home_school_number_per_sector.update_traces(textposition="outside")
home_school_number_per_sector.update_layout(yaxis=dict(visible=True), xaxis=dict(visible=False))
home_school_number_per_sector.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 16, "b": 8},  # Optional: Adjust margins
    paper_bgcolor='rgba(0, 0, 0, 0)', 
    plot_bgcolor='rgba(0, 0, 0, 0)',   
    yaxis=dict(showticklabels=True),
    legend=dict(
        orientation="h",  # Horizontal legend
        yanchor="bottom",  # Align legend at the bottom
        y=-0.2,  # Position it below the chart
        xanchor="center",  # Center it horizontally
        x=0.5  # Align it to the center
    )
)

# ----------------------------------------------------------
# Gender Distribution



