import re, os, sys
import dash
from dash import dcc, html

from numpy import average
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from config import project_root
from utils.get_data import auto_extract


# -- Create the appropriate plot
dataframe = auto_extract(['counts'], is_specific=False)

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
                                        'ELEM': '#FF899A', 
                                        'JHS': '#E11C38', 
                                        'SHS': '#930F22'    
                                    }
                            )
home_enrollment_per_region

# Layout configs
home_enrollment_per_region.update_layout(yaxis=dict(visible=True), xaxis=dict(visible=False))
home_enrollment_per_region.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 16, "b": 8},  # Optional: Adjust margins
    paper_bgcolor='rgba(0, 0, 0, 0)', 
    plot_bgcolor='rgba(0, 0, 0, 0)',   
    yaxis=dict(showticklabels=True),
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

shs_df = auto_extract(['strand', 'track', 'shs_grade', 'counts'], is_specific=False)
shs_df

es_count = dataframe[dataframe['school-level'] == 'ELEM']['counts'].sum()
shs_count = dataframe[dataframe['school-level'] == 'SHS']['counts'].sum()

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
# Number Format
import math

def smart_truncate_number(n):
    if n < 1000:
        return str(n)

    # Handle Millions (M)
    if n >= 1_000_000:
        base = n / 1_000_000  # Get the number in millions
        truncated = math.floor(base * 10) / 10  # Truncate to 1 decimal
        return f"{int(truncated) if truncated.is_integer() else truncated}M"

    # Handle Thousands (k)
    elif n >= 1000:
        base = n / 1000  # Get the number in thousands
        truncated = math.floor(base * 10) / 10  # Truncate to 1 decimal
        return f"{int(truncated) if truncated.is_integer() else truncated}k"

# ----------------------------------------------------------
# School Distribution Across Sectors

df4 = auto_extract(['sector'], is_specific=False)
df4

grouped_by_sectors = df4.groupby("sector")
sector_counts = grouped_by_sectors.size().reset_index(name="count")

home_school_number_per_sector = px.bar(sector_counts, x="sector", y="count",
            #  title="Distribution of Schools Across Sectors",
             text="count",
             orientation="v",
             color="sector",
             color_discrete_map={
                'Private': '#037DEE', 
                'Public': '#037DEE', 
                'SUCsLUCs': '#037DEE'    
             })

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

home_school_number_per_sector

# ----------------------------------------------------------
# Gender Distribution
# Group the original dataframe to sum by gender

grouped_by_gender = dataframe.groupby(['gender'], as_index=False)['counts'].sum()

colors = ['#FF5B72', '#5DB7FF']

# Create half-donut chart
home_gender_distribution = go.Figure(go.Pie(
    labels=grouped_by_gender['gender'],
    values=grouped_by_gender['counts'],
    hole=0.65,
    direction='clockwise',
    sort=False,
    textinfo='label+percent',
    marker=dict(colors=colors)
))

home_gender_distribution.update_layout(
    showlegend=False,
    margin=dict(t=0, b=0, l=0, r=0),
    annotations=[dict(text='Gender Distribution',
                      x=0.5,
                      y=0.5,
                      font_size=20,
                      showarrow=False)],
)

home_gender_distribution.update_traces(rotation=180)
home_gender_distribution

total_male_count = grouped_by_gender.loc[grouped_by_gender['gender'] == 'M', 'counts'].values[0]
total_male_count = smart_truncate_number(total_male_count)
total_male_count

total_female_count = grouped_by_gender.loc[grouped_by_gender['gender'] == 'F', 'counts'].values[0]
total_female_count = smart_truncate_number(total_female_count)
total_female_count

# ----------------------------------------------------------
# Regional Distribution



# ----------------------------------------------------------
# Total Number of Schools Available

number_of_schools = df4["beis_id"].count()
number_of_schools = smart_truncate_number(number_of_schools)
number_of_schools

# ----------------------------------------------------------
# Enrollees per Education Level

grouped_by_school_level = dataframe.groupby('school-level', as_index=False)['counts'].sum()

total_es_count = grouped_by_school_level.loc[grouped_by_school_level["school-level"] == "ELEM", 'counts'].values[0]
total_es_count = smart_truncate_number(total_es_count)

total_jhs_count = grouped_by_school_level.loc[grouped_by_school_level["school-level"] == "JHS", 'counts'].values[0]
total_jhs_count = smart_truncate_number(total_jhs_count)

total_shs_count = grouped_by_school_level.loc[grouped_by_school_level["school-level"] == "SHS", 'counts'].values[0]
total_shs_count = smart_truncate_number(total_shs_count)