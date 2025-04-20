from enum import auto
import re, os, sys
from tkinter import font
import dash
from dash import dcc, html

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.reports.location_chart import FILTERED_DF

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from config import project_root
from utils.get_data import auto_extract

"""
    Analytics/SHS Tracks and Strands Charts and Indicator
"""

#################################################################################
##                     MAIN DATAFRAME BASED FROM THE QUERY                     ##
#################################################################################

# ## -- This only a temporary dataframe for testing your charts, you can change it
FILTERED_DF = dataframe = auto_extract(['sub_class', 'track', 'counts'], is_specific=False)
FILTERED_DF

HM_CBC_DF = dataframe = auto_extract(['counts', 'region', 'sub_class', 'mod_coc', 'track'], is_specific=False)

# Rename values in subclass, type, and sector
subclass_rename = {
    'LUC': 'LUC Managed',
    'Non-Sectarian ': 'Non-Sectarian',
    'SCHOOL ABROAD': 'School Abroad',
    'Sectarian ': 'Sectarian'
}
type_rename = {
    'School with no Annexes' : 'No Annexes', 
    'Mother school': 'Mother School',
    'Annex or Extension school(s)': 'Annex/Extension', 
    'Mobile School(s)/Center(s)': 'Mobile School'
}
sector_rename = {
    'SUCsLUCs': 'SUCs/LUCs'
}

# Apply renaming if columns exist
if 'sub_class' in HM_CBC_DF.columns:
    HM_CBC_DF['sub_class'] = HM_CBC_DF['sub_class'].map(subclass_rename).fillna(HM_CBC_DF['sub_class'])

if 'type' in HM_CBC_DF.columns:
    HM_CBC_DF['type'] = HM_CBC_DF['type'].map(type_rename).fillna(HM_CBC_DF['type'])

if 'sector' in HM_CBC_DF.columns:
    HM_CBC_DF['sector'] = HM_CBC_DF['sector'].map(sector_rename).fillna(HM_CBC_DF['sector'])

HM_CBC_DF

# ## -- Check the document for all valid columns and structurette
# ## -- Dont change the all caps variables
#################################################################################




#################################################################################
#################################################################################
## -- EXAMPLE CHHART

# # Manipulated Data for charts
# query = FILTERED_DF[['grade']][:]

# query['school-level'] = query['grade'].apply(
#     lambda x: 'JHS' if x in ['G7', 'G8', 'G9', 'G10', 'JHS'] else ('SHS' if x in ['G11', 'G12'] else 'ELEM')
# )

# query = query.groupby(['school-level', 'grade']).size().reset_index(name='school_count')

# # Ploting
# sample_chart = px.bar(
#     query,
#     x="school_count", 
#     y="grade",
#     color='school-level',
#     color_discrete_map={
#         'ELEM': '#FF899A', 
#         'JHS': '#E11C38', 
#         'SHS': '#930F22'
#     }
# )
# sample_chart

# sample_chart.update_layout(
#     autosize=True,
#     margin={"l": 8, "r": 8, "t": 8, "b": 8},
# )



#################################################################################
#################################################################################


## -- FIND YOUR CHARTS HERE:

################################################################################
##  --- Total schools per subclass
#################################################################################
subclass_df1 = (
    FILTERED_DF.groupby('sub_class')
    .agg(
        school_count=('beis_id', 'nunique'),
        counts=('counts', 'sum'),  
    )
    .reset_index()
)

total_schools_per_subclass = px.bar(subclass_df1, 
    x='school_count', 
    y='sub_class', 
    title='Total Number of Schools per Subclass',
    labels={'sub_class': 'Subclass', 'school_count': 'Number of Schools'},
    text='school_count',
    color='sub_class',
    color_discrete_sequence=['#012C53','#023F77','#02519B','#0264BE',
                             '#0377E2','#2991F1','#4FA4F3','#74B8F6','#9ACBF8'],
)    
total_schools_per_subclass.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 40, "b": 8},
    yaxis=dict(showticklabels=True),
    showlegend=False
)
#################################################################################




#################################################################################
##  --- Enrollment distribution by subclass
#################################################################################
distrib_by_subclass = px.pie(FILTERED_DF, 
    values='counts',
    names='sub_class', 
    color='sub_class',
    color_discrete_map={
        'DOST Managed': '#012C53',
        'DepED Managed': '#023F77',
        'LUC Managed': '#02519B',
        'Local International School': '#0264BE',
        'Non-Sectarian': '#0377E2',
        'Other GA Managed': '#2991F1',
        'School Abroad': '#4FA4F3',
        'SUC Managed': '#74B8F6',
        'Sectarian': '#9ACBF8'
    }
)
distrib_by_subclass.update_traces(
    textinfo='label+percent',
    textfont_size=9,
    pull=[0.1 if x != 'DepED Managed' else 0 for x in FILTERED_DF['sub_class']],
    marker=dict(line=dict(color='#FFFFFF', width=2)),
    rotation=315
)
distrib_by_subclass.update_layout(
    autosize=True,
    showlegend=True,
    margin={"l": 8, "r": 8, "t": 40, "b": 8},
    title={'text': 'Enrollment Distribution by Subclass','font': {'color': '#3C6382'}},
)
#################################################################################



#################################################################################
##  --- Average enrollment per school
#################################################################################
subclass_df2 = FILTERED_DF.groupby(['sub_class','beis_id'], as_index=False)['counts'].sum()
avg_enrollment = subclass_df2.groupby('sub_class', as_index=False)['counts'].mean().round(0).astype({'counts': int})

def get_avg_enroll(subclass_name):
    row = avg_enrollment.loc[avg_enrollment['sub_class'] == subclass_name, 'counts']
    return row.values[0] if not row.empty else None

avg_enroll_dost = get_avg_enroll('DOST Managed')
avg_enroll_deped = get_avg_enroll('DepED Managed')
avg_enroll_luc = get_avg_enroll('LUC Managed')
avg_enroll_int = get_avg_enroll('Local International School')
avg_enroll_nonsec = get_avg_enroll('Non-Sectarian')
avg_enroll_ga = get_avg_enroll('Other GA Managed')
avg_enroll_abroad = get_avg_enroll('School Abroad')
avg_enroll_suc = get_avg_enroll('SUC Managed')
avg_enroll_sec = get_avg_enroll('Sectarian')
#################################################################################



#################################################################################
##  --- Student-to-school ratio
#################################################################################
student_school_ratio = px.scatter(subclass_df1, 
    x="counts", 
    y="school_count",
    color='sub_class',
    color_discrete_sequence=['#012C53','#023F77','#02519B','#0264BE',
                             '#0377E2','#2991F1','#4FA4F3','#74B8F6','#9ACBF8'],
)
student_school_ratio.update_traces(marker=dict(size=12))
student_school_ratio.update_layout(
    title={
        'text': "Student-to-School Ratio",
        'font': {'color': '#3C6382'}
    },xaxis_title='Number of Enrolled Students',
    yaxis_title='Number of Schools',
    margin={"l": 0, "r": 0, "t": 40, "b": 50},
    scattermode="group",
    legend={
        'title': {'text': "Subclassifications", 'font': {'color': '#667889'}},
        'orientation': 'h', 
        'yanchor': 'bottom',
        'y': -10, 
        'xanchor': 'center',
        'x': 0.5 
    }
)
#################################################################################



#################################################################################
##  --- Subclass vs school type
#################################################################################
subclass_df3 = (
    FILTERED_DF.groupby(['sub_class','type'])
    .agg(
        school_count=('beis_id', 'nunique'),
        counts=('counts', 'sum'),  
    )
    .reset_index()
)

subclass_vs_school_type = px.bar(
    subclass_df3,
    x='school_count',
    y='sub_class',
    orientation='h',
    color='type',
    labels={'sub_class': 'Subclass', 'school_count': 'Number of Schools', 'type': 'School Type'},
    color_discrete_sequence=['#921224', '#D61B35', '#EA6074', '#F3A4AF'],
)

subclass_vs_school_type.update_layout(
    title={
        'text': "Number of Schools by School Type",
        'font': {'color': '#3C6382'}
    },
    xaxis={
        'title': {'text': "Number of Schools", 'font': {'color': '#667889'}},
        'tickfont': {'color': '#667889'}
    },
    yaxis={
        'title': {'text': "Subclassification", 'font': {'color': '#667889'}},
        'tickfont': {'color': '#667889'}
    },                              
    legend={
        'title': {'text': "School Type", 'font': {'color': '#667889'}},
        'font': {'color': '#667889'},
        'orientation': 'h', 
        'yanchor': 'bottom',
        'y': -0.2, 
        'xanchor': 'center',
        'x': 0.5 
    },
    margin=dict(l=0, r=0, t=40, b=20)
)
subclass_vs_school_type
#################################################################################



#################################################################################
##  --- Sector affiliation
#################################################################################
subclass_df4 = FILTERED_DF.groupby(['sub_class', 'sector']).agg(
    school_count=('beis_id', 'nunique'),
    total_enrollees=('counts', 'sum')
).reset_index()
subclass_df4.sort_values(by='sub_class', inplace=True)

sector_affiliation = go.Figure(data=[go.Table(
    header=dict(
        values=["Subclass", "Sector", "No. of Schools", "Total Enrollees"],
        fill_color='#EA6074',
        align='left',
        font=dict(size=10)
    ),
    cells=dict(
        values=[
            subclass_df4['sub_class'],
            subclass_df4['sector'],
            subclass_df4['school_count'],
            subclass_df4['total_enrollees']
        ],
        fill_color='#F8C6CD',
        align='left',
        font=dict(size=9)
    )
)])
sector_affiliation.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 40, "b": 8},
    title={'text': "Sector Affiliation",'font': {'color': '#3C6382'}},
)
#################################################################################



#################################################################################
##  --- Regional distribution/ which subclass has the highest number of schools per loc
#################################################################################
# Assuming FILTERED_DF is already defined
query2 = HM_CBC_DF[['region', 'sub_class']][:]

# Count the number of schools per sub_class per region
query2 = query2.groupby(['region', 'sub_class']).size().reset_index(name='school_count')

# Pivot the data to wide format for heatmap
heatmap_df = query2.pivot(index='region', columns='sub_class', values='school_count').fillna(0)

# Reset index for Plotly compatibility
heatmap_df = heatmap_df.reset_index().melt(id_vars='region', var_name='sub_class', value_name='school_count')

# Create heatmap with custom reversed secondary shades palette
subclass_heatmap = px.density_heatmap(
    heatmap_df,
    x='sub_class',
    y='region',
    z='school_count',
    color_continuous_scale=[
        '#F3A4AF',  # Lightest - secondary-shades-9
        '#EF8292',
        '#EA6074',
        '#E63E56',
        '#D61B35',
        '#B4162D',
        '#921224',
        '#710E1C',
        '#4F0A14'   # Darkest - secondary-shades-1
    ],
    text_auto=False
)

# Update layout for improved visuals
subclass_heatmap.update_layout(
    title=dict(
        text='Regional Distribution of Schools',
        font=dict(
            family='Inter Bold',
            size=14,
            color='#04508c'
        )
    ),
    xaxis=dict(
        tickangle=45,
        tickfont=dict(size=9),
        title=''
    ),
    yaxis=dict(
        tickfont=dict(size=9),
        title='',
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text='Schools',
            font=dict(
                family='Inter Medium',
                size=10
            )
        )
    ),
    font=dict(size=11),
    autosize=True,
    margin={"l": 100, "r": 10, "t": 40, "b": 50}
)





#################################################################################



#################################################################################
##  --- MCOC breakdown/which subclass offers which program types
#################################################################################
# Filter the dataframe to include only the required columns
mcoc_df = HM_CBC_DF[['mod_coc', 'counts', 'sub_class']]

# Group by 'mod_coc' and 'sub_class' to aggregate the counts
mcoc_grouped = mcoc_df.groupby(['mod_coc', 'sub_class']).sum().reset_index()

# Truncate counts directly in the DataFrame
mcoc_grouped['counts'] = mcoc_grouped['counts'].apply(
    lambda count: f"{count/1_000_000:.1f}M" if count >= 1_000_000 else
                  f"{count/1_000:.1f}K" if count >= 1_000 else
                  str(count)
)

# Sort the DataFrame by counts to ensure the lowest values are at the bottom
mcoc_grouped['numeric_counts'] = mcoc_df.groupby(['mod_coc', 'sub_class'])['counts'].transform('sum')
mcoc_grouped = mcoc_grouped.sort_values(by='numeric_counts')

# Create a clustered bar chart with default discrete color sequence
subclass_clustered = px.bar(
    mcoc_grouped,
    x='mod_coc',  # Set mod_coc as x-axis
    y='counts',  # Set counts as y-axis
    color='sub_class',  # Clustered by subclass
    barmode='group',  # Grouped bar chart
    color_discrete_sequence=[
        "#012C53", "#023F77", "#02519B", "#0264BE", "#0377E2",
        "#2991F1", "#4FA4F3", "#74B8F6", "#9ACBF8", "#C0DFFB", "#E6F2FD"
    ]   # Apply the color scheme
)

# Update the layout for better readability
subclass_clustered.update_layout(
    title=dict(
        text='Program Types',
        font=dict(
            family='Inter Bold',  # Use the 'Inter Bold' font face
            size=14,  # Font size
            color= '#04508c'
        ),
    ),
    xaxis=dict(
        title='',  # Set x-axis title
        tickangle=45,  # Rotate x-axis labels for better readability
        tickfont=dict(
            family='Inter Medium',  # Use the 'Inter Medium' font face
            size=8
        )
    ),
    yaxis=dict(
        title='',  # Set y-axis title
        tickfont=dict(
            family='Inter Medium',  # Use the 'Inter Medium' font face
            size=8
        )
    ),
    font=dict(size=11),  # General font size
    autosize=False,
    width=300,  # Increase the width of the chart
    height=200,  # Increase the height of the chart
    margin={"l": 70, "r": 10, "t": 50, "b": 10},  # Adjust margins
    showlegend=False,
    bargap=0.1,
    bargroupgap=0.0,  # Adjust the gap between bars in the same group
)





#################################################################################



#################################################################################
##  --- Enrollment in shs tracks across subclass
#################################################################################
# Filter the dataframe to include only SHS tracks and subclasses
shs_tracks_df = FILTERED_DF[['track', 'sub_class']]

# Remove rows with missing values in 'track' or 'sub_class'
shs_tracks_df = shs_tracks_df.dropna(subset=['track', 'sub_class'])

# Group by 'track' and 'sub_class' and count the entries
shs_tracks_grouped = shs_tracks_df.groupby(['track', 'sub_class']).size().reset_index(name='counts')

# Truncate 'track' and 'sub_class' values for better readability
shs_tracks_grouped['track'] = shs_tracks_grouped['track'].str.slice(0, 20)
shs_tracks_grouped['sub_class'] = shs_tracks_grouped['sub_class'].str.slice(0, 15)

# Create a clustered bar chart for SHS tracks and subclasses
subclass_clustered_tracks = px.bar(
    shs_tracks_grouped,
    x='track',
    y='counts',
    color='sub_class',
    barmode='group',
    title='Enrollment in SHS Tracks Across Subclass'
)

# Update chart layout for improved readability
subclass_clustered_tracks.update_layout(
    title=dict(
        text='SHS Tracks Enrollment',
        font=dict(family='Inter Bold', size=14, color='#04508c'),
        x=0  # Left align the title
    ),
    xaxis=dict(
        title='',
        tickangle=45,
        tickfont=dict(size=10, family='Inter Medium')
    ),
    yaxis=dict(
        title='',
        tickfont=dict(size=10, family='Inter Medium')
    ),
    showlegend=True,  # Display legend for clarity
    legend_title=None,  # Remove legend title (sub_class)
    font=dict(size=11, family='Inter Medium'),
    autosize=True,
    margin={"l": 50, "r": 10, "t": 50, "b": 40}  # Adjust margins
)








#################################################################################

#################################################################################
##  --- % schools offering ‘all offerings’ for the entire mod_coc
#################################################################################

# Group by sub_class, calculate total and 'All Offering' counts
grouped = HM_CBC_DF.groupby('sub_class')

# Total schools per sub_class
total_counts = grouped['counts'].sum()

# Schools offering "All Offering" per sub_class
all_offerings_counts = HM_CBC_DF[HM_CBC_DF['mod_coc'] == 'All Offering'].groupby('sub_class')['counts'].sum()

# Calculate % of All Offering per sub_class
percentage_per_subclass = (all_offerings_counts / total_counts) * 100

# Drop NaNs (in case some subclasses had no 'All Offering')
percentage_per_subclass = percentage_per_subclass.dropna()

# Get top sub_class and its percentage
top_subclass = percentage_per_subclass.idxmax()
top_percentage = percentage_per_subclass.max()

# Create the figure
subclass_firstindicator = go.Figure()

# Add the indicator (number + delta)
subclass_firstindicator.add_trace(go.Indicator(
    mode="number+delta",
    value=top_percentage,
    number={
        "suffix": "%",
        "font": {
            "size": 30,
            "color": "#02519B",
            "family": "Inter Bold, sans-serif"
        }
    },
    delta={
        "reference": 100,
        "relative": False,
        "increasing": {"color": "#03C988"},
        "decreasing": {"color": "#FF6B6B"},
    },
    domain={'x': [0, 1], 'y': [0.35, 0.75]}  # Centered vertically
))

# Add subclass name as annotation below the indicator
subclass_firstindicator.update_layout(
    annotations=[
        dict(
            text=(
                f"<span style='font-family:Inter Medium, sans-serif; font-size:10px;'>"
                f"<b>Top All Program Offering:</b> <br> {top_subclass}</span>"
            ),
            x=0.5,
            y=0.20,
            xanchor='center',
            yanchor='top',
            showarrow=False,
        )
    ],
    margin=dict(t=10, b=10, l=10, r=10),
    paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#012C53"),
    autosize=True,
)













#################################################################################



#################################################################################
##  --- % schools offering shs per subclass
#################################################################################
# Get all unique SHS tracks
unique_tracks = FILTERED_DF['track'].unique()
total_tracks = len(unique_tracks)

# Count the unique tracks offered per sub_class
tracks_per_subclass = FILTERED_DF.groupby('sub_class')['track'].nunique()

# Calculate the percentage of tracks offered for each sub_class
percentage_tracks_per_subclass = (tracks_per_subclass / total_tracks) * 100

# Find the sub_class with the highest percentage
top_subclass = percentage_tracks_per_subclass.idxmax()
top_percentage = percentage_tracks_per_subclass.max()

subclass_secondindicator = go.Figure()

subclass_secondindicator.add_trace(go.Indicator(
    mode="number",
    value=top_percentage,
    number={
        "suffix": "%",
        "font": {
            "size": 30,
            "color": "#02519B",
            "family": "Inter Bold, sans-serif"
        }
    },
    domain={'x': [0, 1], 'y': [0.5, 1]}  # Indicator takes the upper half
))

subclass_secondindicator.update_layout(
    annotations=[
        dict(
            text=(
                f"<span style='font-family:Inter Medium, sans-serif; font-size:10px;'>"
                f"<b>Top SHS Track Coverage:</b><br>{top_subclass}</span>"
            ),
            x=0.5,
            y=0.4,  # Just below the number
            xanchor='center',
            yanchor='top',
            showarrow=False,
        )
    ],
    margin=dict(t=10, b=10, l=10, r=10),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#012C53"),
    autosize=True,
)






#################################################################################