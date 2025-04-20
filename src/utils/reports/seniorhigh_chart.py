import re, os, sys
import dash
from dash import dcc, html

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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
# FILTERED_DF = dataframe = auto_extract(['counts'], is_specific=False)
# FILTERED_DF

FILTERED_DF = dataframe = auto_extract(['shs_grade', 'sector'], is_specific=False)
FILTERED_DF
# ## -- Check the document for all valid columns and structurette
# ## -- Dont change the all caps variables
#################################################################################




#################################################################################
#################################################################################
## -- EXAMPLE CHHART

# Manipulated Data for charts
query = FILTERED_DF[['grade']][:]

query['school-level'] = query['grade'].apply(
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
sample_chart

sample_chart.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 8, "b": 8},  # Optional: Adjust margins
)



#################################################################################
#################################################################################


## -- FIND YOUR CHARTS HERE:

################################################################################
##  --- Distribution of enrollees per track
#################################################################################
# Group and prepare the data
enrollees_distribution = FILTERED_DF.groupby(['track'])['counts'].sum().reset_index()

# Create the horizontal bar chart
seniorhigh_distri_per_track = px.bar(
    enrollees_distribution, 
    x='counts', 
    y='track', 
    orientation='h', 
    labels={'counts': 'Number of Students', 'track': 'Track', 'color': '#667889'}
)

# Update layout to ensure all y-axis labels show
seniorhigh_distri_per_track.update_layout(
    bargap=0.2,
    autosize=True,
    margin=dict(l=80, r=10, t=50, b=10),  
    title={
        'text': 'Distribution of SHS Enrollees per Track',
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'size': 14,
            'color': '#3C6382'
        },
    },
    yaxis=dict(
        automargin=True,          
        tickfont=dict(size=12),   
    ),
)

# Keep layout responsive
seniorhigh_distri_per_track.update_layout(
    uirevision='true',
)

# Change the color of the bars
seniorhigh_distri_per_track.update_traces(marker_color='#EF8292')

# Display the chart
seniorhigh_distri_per_track






#################################################################################




#################################################################################
##  --- Ratio enrollment in Academic vs. non-Academic tracks
#################################################################################
# Count the number of students in each 'track'
track_counts = FILTERED_DF.groupby('track').size().reset_index(name='student_count')

# Get the acad_count and non_acad_count
acad_count = track_counts.loc[track_counts['track'] == 'acad', 'student_count'].sum()
non_acad_count = track_counts.loc[track_counts['track'].isin(['TVL', 'ARTS', 'SPORTS']), 'student_count'].sum()

# Create the Donut Chart
seniorhigh_ratio_enrollment = go.Figure(
    data=[go.Pie(
        labels=['Academic', 'Non-Academic'],
        values=[acad_count, non_acad_count],
        hole=0.7,  
        marker=dict(colors=['#5DB7FF', '#FF5B72']),
        textinfo='none',
        hoverinfo='label+value+percent',
        direction='clockwise',
        sort=False,
        domain={'x': [0, 1], 'y': [0, 1]},
    )]
)

# Update layout for true maximization
seniorhigh_ratio_enrollment.update_layout(
    autosize=True,
    margin=dict(t=0, r=0, b=0, l=0),  
    showlegend=False,
    annotations=[
        dict(
            text="Academic<br>vs.<br>Non-Academic",
            x=0.5, y=0.5,
            font=dict(size=14, color='#3C6382'),  
            showarrow=False,
            align='center',
            xanchor='center',
            yanchor='middle'
        )
    ]
)
seniorhigh_ratio_enrollment







#################################################################################



#################################################################################
##  --- Most and least enrolled  (strand)
#################################################################################
track_counts = FILTERED_DF.groupby('strand')['counts'].sum().reset_index()
most_populated = track_counts.sort_values('counts', ascending=False).iloc[0]
least_populated = track_counts.sort_values('counts', ascending=True).iloc[0]

# Data for tables
most_populated_table = go.Table(
    header=dict(
        values=["Most Populated"],
        fill_color='#E63E56',
        align='center',
        font=dict(size=14, color='#FFFFFF')
    ),
    cells=dict(
        values=[[f"<b>{most_populated['strand']}</b>", f"<b>{most_populated['counts']}</b> students"]],
        align='center',
        font=dict(size=14, color='#FFFFFF'),
        height=35,
        fill=dict(color=['#EF8292', '#EF8292'])
    ),
    domain=dict(x=[0, 1], y=[0.55, 1])
)

least_populated_table = go.Table(
    header=dict(
        values=["Least Populated"],
        fill_color='#E63E56',
        align='center',
        font=dict(size=14, color='#FFFFFF')
    ),
    cells=dict(
        values=[[f"<b>{least_populated['strand']}</b>", f"<b>{least_populated['counts']}</b> students"]],
        align='center',
        font=dict(size=14, color='#FFFFFF'),
        height=35,
        fill=dict(color=['#EF8292', '#EF8292'])
    ),
    domain=dict(x=[0, 1], y=[0, 0.45])
)

# Combine tables in one figure with autosizing
seniorhigh_most_least_enrolled = go.Figure(data=[most_populated_table, least_populated_table])
seniorhigh_most_least_enrolled.update_layout(
    autosize=True,
    margin=dict(t=10, b=10, l=10, r=10)
)
seniorhigh_most_least_enrolled


#################################################################################



#################################################################################
##  --- Gender Distribution
#################################################################################
# Group the data by 'strand' and 'gender' and sum the counts
track_gender = FILTERED_DF.groupby(['strand', 'gender'])['counts'].sum().reset_index()

# Create the horizontal bar chart
seniorhigh_gender_distri = px.bar(
    track_gender,
    x='counts',
    y='strand',
    color='gender',
    orientation='h',
    barmode='group',
    labels={'strand': 'Strand', 'counts': 'Number of Students', 'gender': 'Gender'},
    color_discrete_sequence=['#5DB7FF', '#FF5B72']
)

# Update layout to maximize chart space and reduce label sizes
seniorhigh_gender_distri.update_layout(
    autosize=True,
    margin=dict(l=60, r=10, t=50, b=20),
    title={
        'text': "Distribution by<br>Strand and Gender",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': '#3C6382', 'size': 14}
    },
    xaxis={
        'title': {'text': "Number of Students", 'font': {'color': '#667889', 'size': 11}},
        'tickfont': {'color': '#667889', 'size': 10},
    },
    yaxis={
        'title': {'text': "Strand", 'font': {'color': '#667889', 'size': 11}},
        'tickfont': {'color': '#667889', 'size': 10},
        'automargin': True
    },
    legend={
        'title': {'text': "Gender", 'font': {'color': '#667889', 'size': 10}},
        'font': {'color': '#667889', 'size': 10}
    },
    bargap=0.3,
    bargroupgap=0.05,
    uirevision='true',
)
seniorhigh_gender_distri




#################################################################################



#################################################################################
##  --- Differences in the number of schools offering each track
#################################################################################
# Group data by track and sector, counting unique schools
FILTERED_DF = dataframe = auto_extract(['shs_grade', 'sector'], is_specific=False)
FILTERED_DF = FILTERED_DF[FILTERED_DF['counts'] != 0]
school_count = FILTERED_DF.groupby(['track', 'sector'])['beis_id'].nunique().reset_index(name='school_count')

# Create horizontal stacked bar chart
seniorhigh_school_offering_per_track_by_sector = px.bar(
    school_count,
    x='school_count',
    y='track',
    color='sector',
    orientation='h',
    labels={'school_count': 'Number of Schools', 'track': 'Track', 'sector': 'Sector'},
    color_discrete_sequence=['#02519B', '#0377E2', '#4FA4F3', '#9ACBF8'],
    title="Number of Schools Offering Each Track by Sector"
)

# Update layout
seniorhigh_school_offering_per_track_by_sector.update_layout(
    title={
        'text': "Number of Schools<br>Offering Each Track by Sector",
        'x': 0.5,
        'font': {'color': '#3C6382', 'size': 14}
    },
    xaxis={
        'title': {'text': "Number of Schools", 'font': {'color': '#667889'}},
        'tickfont': {'color': '#667889'},
        'tickformat': '~s',  
        'tickangle': 0       
    },
    yaxis={
        'title': {'text': "Track", 'font': {'color': '#667889'}},
        'tickfont': {'color': '#667889'}
    },
    legend={
        'title': {'text': "Sector", 'font': {'color': '#667889'}},
        'font': {'color': '#667889'}
    },
    bargap=0.6,
    autosize=True,
    margin=dict(l=80, r=40, t=60, b=40)
)
seniorhigh_school_offering_per_track_by_sector








#################################################################################



#################################################################################
##  --- Which SHS tracks are least offered but in high demand
#################################################################################
# Group by track to get supply and demand
grouped = FILTERED_DF.groupby('track').agg(
    offerings=('enroll_id', 'count'),    
    total_demand=('counts', 'sum')       
).reset_index()

# Define custom color palette
custom_colors = ['#FFB700', '#F9F521', '#89FE2A', '#00F2FF', '#00CCFF', '#1389F0', '#0C6DC1', '#074889']

# Create the scatter plot
seniorhigh_least_offered_high_demand = px.scatter(
    grouped,
    x='offerings',
    y='total_demand',
    color='track',
    labels={
        'offerings': 'Number of Offerings (Supply)',
        'total_demand': 'Student Demand',
        'track': 'SHS Track',
    },
    color_discrete_sequence=custom_colors
)

# Update layout for full responsiveness with legend on the right
seniorhigh_least_offered_high_demand.update_layout(
    autosize=True,
    margin=dict(l=60, r=120, t=60, b=60),  
    title={
        'text': 'Relationship between<br>Student Demand and Track Supply',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': '#3C6382', 'size': 14}
    },
    xaxis={
        'title': {'text': 'Number of Offerings (Supply)', 'font': {'color': '#667889', 'size': 12}},
        'tickfont': {'color': '#667889'},
        'automargin': True
    },
    yaxis={
        'title': {'text': 'Student Demand', 'font': {'color': '#667889', 'size': 12}},
        'tickfont': {'color': '#667889'},
        'automargin': True
    },
    legend={
        'title': {'text': 'SHS Track', 'font': {'color': '#667889'}},
        'font': {'color': '#667889'},
        'orientation': 'v',
        'yanchor': 'middle',
        'y': 0.5,
        'xanchor': 'left',
        'x': 1.05
    }
)

seniorhigh_least_offered_high_demand






#################################################################################



#################################################################################
##  --- How many schools offer each SHS track per region
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- Which SHS tracks are more prevalent in each sector
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- Do mother schools or annexes offer a wider range of SHS tracks
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################

