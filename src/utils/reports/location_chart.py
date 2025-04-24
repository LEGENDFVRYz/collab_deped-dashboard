from random import sample
import re, os, sys
import dash
from dash import dcc, html

import math
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import false

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from config import project_root
from utils.get_data import auto_extract


"""
    Analytics/Location Charts and Indicator
    
"""


#################################################################################
##                     MAIN DATAFRAME BASED FROM THE QUERY                     ##
#################################################################################

# ## -- This only a temporary dataframe for testing your charts, you can change it
FILTERED_DF = dataframe = auto_extract(['counts'], is_specific=False)
FILTERED_DF

# ## -- Check the document for all valid columns and structurette
# ## -- Dont change the all caps variables
#################################################################################



#################################################################################
#################################################################################
## -- EXAMPLE CHHART

# Manipulated Data for charts
query = FILTERED_DF[['grade']][:]

query.loc[:, 'school-level'] = query['grade'].apply(
    lambda x: 'JHS' if x in ['G7', 'G8', 'G9', 'G10', 'JHS'] else ('SHS' if x in ['G11', 'G12'] else 'ELEM')
)

query = query.groupby(['school-level', 'grade']).size().reset_index(name='school_count')

# Ploting
sample_chart = px.bar(
    query,
    x="school_count", 
    y="grade",
    color='school-level',
    color_discrete_map={
        'ELEM': '#FF899A', 
        'JHS': '#E11C38', 
        'SHS': '#930F22'
    }
)
sample_chart.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 12, "b": 8},  # Optional: Adjust margins
)
sample_chart

#################################################################################
#################################################################################




## -- FIND YOUR CHARTS HERE:

################################################################################
##  --- CHART: Distribution of enrollees per location 
#################################################################################
# chart_x = px.bar(filtered_df, )

# from utils.reports.home_enrollment_per_region import smart_truncate_number

# total_gender_region = dataframe = auto_extract(['region', 'gender', 'counts'], is_specific=False)
# total_gender_region

# # Step 1: Group by region and gender
# gender_region = total_gender_region.groupby(['region', 'gender'])['counts'].sum().reset_index()

# # Step 2: Define brand colors
# brand_colors = {
#     'M': '#037DEE',
#     'F': '#E11C38'
# }

# # Step 3: Create the stacked bar chart
# gender_region_fig = px.bar(
#     gender_region,
#     x='counts',
#     y='region',
#     color='gender',
#     orientation='h',
#     barmode='stack',
#     labels={'counts': 'Number of Enrollees', 'region': 'Region', 'gender': 'Gender'},
#     color_discrete_map=brand_colors
# )

# # Step 4: Calculate total per region for annotations
# region_totals = gender_region.groupby('region')['counts'].sum().reset_index()

# # Step 5: Add truncated total annotations using your function
# for _, row in region_totals.iterrows():
#     short_text = smart_truncate_number(row['counts'])  # Your custom truncation
#     gender_region_fig.add_annotation(
#         x=row['counts'] + 1,
#         y=row['region'],
#         text=short_text,
#         hovertext=str(row['counts']),  # Full raw number on hover
#         showarrow=False,
#         font=dict(color="#04508c", size=12),
#         xanchor="left",
#         yanchor="middle"
#     )

# # Step 6: Customize layout
# gender_region_fig.update_layout(
#     title={
#         'text': "Enrollment Distribution by Region and Gender",
#         'x': 0.5,
#         'xanchor': 'center',
#         'font': {'color': '#04508c'}
#     },
#     xaxis_title="Number of Students",
#     yaxis_title="Region",
#     legend_title="Gender",
#     font=dict(color="#667889"),
#     margin=dict(l=80, r=20, t=50, b=40),
#     plot_bgcolor="#F5FBFF",
#     paper_bgcolor="#F5FBFF",
# )
# gender_region_fig





#################################################################################




#################################################################################
##  --- CHART: enrollment density (students per location)
#################################################################################
# enrollment_density_chart = []





#################################################################################



#################################################################################
##  --- CHART: school sectors
#################################################################################
# enrollment_density_chart = []





#################################################################################



#################################################################################
##  --- CHART: school sectors
#################################################################################






#################################################################################



#################################################################################
##  --- CHART: Strand preferences per region
#################################################################################
track_pref = dataframe = auto_extract(['strand', 'track', 'region'], is_specific=False)
track_pref

# Step 2: Group and SUM the 'counts' column to get total student enrollment
heatmap_data = track_pref.groupby(['region', 'track'])['counts'].sum().reset_index()

# Step 3: Pivot to form a matrix
heatmap_pivot = heatmap_data.pivot(index='track', columns='region', values='counts').fillna(0)

heatmap_fig = px.imshow(
    heatmap_pivot.values,
    labels=dict(x="Region", y="Track", color="Students Enrolled"),
    x=heatmap_pivot.columns.tolist(),
    y=heatmap_pivot.index.tolist(),
    color_continuous_scale=[
        "#074889", "#0C6DC1", "#1389F0", "#00CCFF", 
        "#00F2FF", "#89FE2A", "#F9F521", "#FFB700"
    ]
)


# Step 5: Improve layout
heatmap_fig.update_layout(
    xaxis_title="Region",
    yaxis_title="Track",
    xaxis=dict(tickangle=45),
    margin={"l": 20, "r": 20, "t": 20, "b": 20}
)
# Step 6: Show the heatmap
heatmap_fig

#################################################################################



#################################################################################
##  --- INDICATOR: Total number of enrollees
#################################################################################


from utils.reports.home_enrollment_per_region import smart_truncate_number

total_enro = dataframe = auto_extract(['counts'], is_specific=False)
total_enro

raw_total_enrollees = dataframe['counts'].sum()
truncated_total_enrollees = smart_truncate_number(raw_total_enrollees)

raw_total_enrollees
truncated_total_enrollees


#################################################################################



#################################################################################
##  --- INDICATOR: Total number of schools
#################################################################################
# total_scho = dataframe = auto_extract(['name', 'counts'], is_specific=False)
# total_scho
# # Count total number of unique schools
# raw_total_schools = dataframe['name'].nunique()
# truncated_total_schools = smart_truncate_number(raw_total_schools)

# raw_total_schools
# truncated_total_schools





#################################################################################



#################################################################################
##  --- TABLE: Total number of schools
#################################################################################

highest_lowest = dataframe = auto_extract(['name', 'counts', 'region'], is_specific=True)
highest_lowest

# Step 1: Group by school and region, summing the counts
aggregated_df = highest_lowest.groupby(['name', 'region'], as_index=False)['counts'].sum()

# Step 2: Get the school with highest and lowest total enrollees
max_row = aggregated_df.loc[aggregated_df['counts'].idxmax()]
min_row = aggregated_df.loc[aggregated_df['counts'].idxmin()]

# Step 3: Combine them into a new DataFrame for visualization
highest_lowest2 = pd.DataFrame([max_row, min_row])

hi_low_fig = go.Figure(data=[go.Table(
    header=dict(
        values=["School Name", "Region", "Total Enrollees"],
        fill_color='#EA6074',
        align='left'
    ),
    cells=dict(
        values=[
            highest_lowest2['name'],
            highest_lowest2['region'],
            highest_lowest2['counts']
        ],
        fill_color='#F8C6CD',
        align='left'
    )
)])


hi_low_fig


#################################################################################