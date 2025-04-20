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
    labels={'counts': 'Number of Students', 'track': 'Track'}
)

seniorhigh_distri_per_track.update_layout(
    bargap=0.4,
    autosize=True,
    title={
        'text': 'Distribution of SHS Enrollees per Track',
        'x': 0.5,
        'xanchor': 'center',
        'font': {
            'size': 20,  
            'color': '#3C6382' 
        },
    }
)
# Change the color of the bars
seniorhigh_distri_per_track.update_traces(marker_color='#2991F1')
seniorhigh_distri_per_track





#################################################################################




#################################################################################
##  --- Ratio enrollment in Academic vs. non-Academic tracks
#################################################################################
# Count the number of students in each 'track'
track_counts = FILTERED_DF.groupby('track').size().reset_index(name='student_count')

# Get the acad_count and non_acad_count based on 'track' values
acad_count = track_counts.loc[track_counts['track'] == 'acad', 'student_count'].sum()
non_acad_count = track_counts.loc[track_counts['track'].isin(['tvl', 'arts', 'sports']), 'student_count'].sum()

# Create the Pie chart
seniorhigh_ratio_enrollment = go.Figure(
    data=[go.Pie(
        labels=track_counts['track'],  
        values=track_counts['student_count'],  
        textinfo='none',
        marker=dict(colors=['#5DB7FF', '#FF5B72']), 
        hoverinfo='label+percent'
    )]
)

# Layout and annotations for the donut chart
seniorhigh_ratio_enrollment.update_layout(
    autosize=True,
    showlegend=False,
    margin=dict(t=20, r=10, b=100, l=10),  
    annotations=[
        # Center donut title
        dict(
            text="Academic<br>vs.<br>Non-Academic",
            x=0.5, y=0.5,
            showarrow=False,
            font_size=16,
            font_color='#3C6382',
            align='center'
        ),
        # Academic number
        dict(
            text=f"<b>{acad_count:,}</b>",
            x=0.15, y=-0.09,
            showarrow=False,
            font_size=16,
            font_color='#3C6382'
        ),
        # Non-Academic number
        dict(
            text=f"<b>{non_acad_count:,}</b>",
            x=0.85, y=-0.09,
            showarrow=False,
            font_size=16,
            font_color='#3C6382'
        ),
        # "students" label
        dict(
            text="students",
            x=0.17, y=-0.15,
            showarrow=False,
            font_size=12,
            font_color='#9DADBD'
        ),
        dict(
            text="students",
            x=0.83, y=-0.15,
            showarrow=False,
            font_size=12,
            font_color='#9DADBD'
        ),
        # Strand labels
        dict(
            text="<b>ACADEMIC</b>",
            x=0.15, y=-0.23,
            showarrow=False,
            font_size=12,
            font_color='#5DB7FF'
        ),
        dict(
            text="<b>NON-ACADEMIC</b>",
            x=0.9, y=-0.23,
            showarrow=False,
            font_size=12,
            font_color='#FF5B72'
        ),
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
    color='gender',  # This will use the color parameter
    orientation='h',
    barmode='group',
    labels={'strand': 'Strand', 'counts': 'Number of Students', 'gender': 'Gender'},
    color_discrete_sequence=['#5DB7FF', '#FF5B72']  # Directly specify the color sequence for Male and Female
)

# Update layout with formatting
seniorhigh_gender_distri.update_layout(
    title={
        'text': "Enrollment Distribution by Strand and Gender",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'color': '#04508c'}
    },
    xaxis={
        'title': {'text': "Number of Students", 'font': {'color': '#667889'}},
        'tickfont': {'color': '#667889'},
    },
    yaxis={
        'title': {'text': "Strand", 'font': {'color': '#667889'}},
        'tickfont': {'color': '#667889'}
    },
    legend={
        'title': {'text': "Gender", 'font': {'color': '#667889'}},
        'font': {'color': '#667889'}
    },
    bargap=0.8,
    bargroupgap=0.1,
    
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
school_count

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

seniorhigh_school_offering_per_track_by_sector.update_layout(
    title={
        'text': "Number of Schools Offering Each Track by Sector",
        'x': 0.5,
        'font': {'color': '#3C6382'}
    },
    xaxis={
        'title': {'text': "Number of Schools", 'font': {'color': '#667889'}},
        'tickfont': {'color': '#667889'}
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
# Step 1: Group by track to get supply and demand
grouped = FILTERED_DF.groupby('track').agg(
    offerings=('enroll_id', 'count'),    
    total_demand=('counts', 'sum')       
).reset_index()

# Step 2: Create the scatter plot (equal-sized circles)
seniorhigh_least_offered_high_demand = px.scatter(
    grouped,
    x='offerings',
    y='total_demand',
    color='track',
    title='Scatter Plot: SHS Tracks - Least Offered but High in Demand',
    labels={
        'offerings': 'Number of Offerings (Supply)',
        'total_demand': 'Student Demand',
        'track': 'SHS Track',
    },
)

# Step 3: Styling
seniorhigh_least_offered_high_demand.update_layout(
    title={
        'text': 'Relationship between Student Demand and Track Supply',
        'x': 0.5,
        'font': {'color': '#3C6382'}
    },
    xaxis={
        'title': {'text': 'Number of Offerings (Supply)', 'font': {'color': '#667889'}},
        'tickfont': {'color': '#667889'}
    },
    yaxis={
        'title': {'text': 'Student Demand', 'font': {'color': '#667889'}},
        'tickfont': {'color': '#667889'}
    },
    legend={
        'title': {'text': 'SHS Track', 'font': {'color': '#667889'}},
        'font': {'color': '#667889'}
    }
)
seniorhigh_least_offered_high_demand






#################################################################################



#################################################################################
##  --- How many schools offer each SHS track per region
#################################################################################
track_pref = dataframe = auto_extract(['beis_id','strand', 'region'], is_specific=True)
track_pref

heatmap_data = track_pref.groupby(['region', 'strand'])['beis_id'].size().reset_index()
heatmap_data.rename(columns={'beis_id': 'school_count'}, inplace=True)


heatmap_pivot = heatmap_data.pivot(index='strand', columns='region', values='school_count').fillna(0)


heatmap_fig = px.imshow(
    heatmap_pivot.values,
    labels=dict(x="Region", y="Track", color="Number of Schools"),
    x=heatmap_pivot.columns.tolist(),
    y=heatmap_pivot.index.tolist(),
    color_continuous_scale=[
        "#FF899A",  # Light pink
        "#E11C38",  # Mid red
        "#930F22"   # Deep red
    ]
)


heatmap_fig.update_layout(
    title="Number of Schools Offering SHS Tracks per Region",
    xaxis_title="Region",
    yaxis_title="SHS Track",
    xaxis=dict(tickangle=45),
    margin={"l": 20, "r": 20, "t": 40, "b": 40}
)

heatmap_fig


#################################################################################



#################################################################################
##  --- Which SHS tracks are more prevalent in each sector
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )
FILTERED_byprevalent = dataframe = auto_extract(['strand', 'sector'], is_specific=True)
FILTERED_nostudents = dataframe = auto_extract(['counts'], is_specific=True)
grade_enrollment2 = FILTERED_nostudents.groupby('grade')['counts'].sum().reset_index()
merged = FILTERED_byprevalent.copy()
merged['counts'] = FILTERED_nostudents['counts']
grouped = merged.groupby(['strand', 'sector'])['counts'].sum().reset_index()

def smart_truncate_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(num)
grouped['counts_text'] = grouped['counts'].apply(smart_truncate_number)

blue_shades = ['#012C53', '#023F77', '#02519B', '#0264BE', '#0377E2']

grouped['counts_text'] = grouped['counts'].apply(smart_truncate_number)

fig = px.bar(
    grouped,
    x='strand',
    y='counts',
    color='sector',
    barmode='group',
    title='Prevalence of SHS Strands by Sector (Based on Student Count)',
    labels={'strand': 'SHS Strand', 'counts': 'Number of Students', 'sector': 'School Sector'},
    color_discrete_sequence=blue_shades,
    text='counts_text'
)

fig.update_traces(textposition='outside')

fig.update_layout(
    xaxis_tickangle=-45,
    legend_title='Sector',
    xaxis_title='SHS Strand',
    yaxis_title='Number of Students',
    margin=dict(l=60, r=40, t=60, b=60)
)

fig

#################################################################################



#################################################################################
##  --- Do mother schools or annexes offer a wider range of SHS tracks
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )
FILTERED_bytype = dataframe = auto_extract(['strand', 'type'], is_specific=True)
FILTERED_bytype 


track_counts = FILTERED_bytype.groupby('type')['strand'].nunique().reset_index()
track_counts.columns = ['School Type', 'Number of strand']


blue_shades = ['#012C53', '#023F77', '#02519B', '#0264BE', '#0377E2']

track_counts = FILTERED_bytype.groupby('type')['strand'].nunique().reset_index()
track_counts.columns = ['School Type', 'Number of strand']

fig = px.bar(
    track_counts,
    x='School Type',
    y='Number of strand',
    title='Number of SHS Strand Offered by Mother Schools vs Annexes',
    color='School Type',
    text='Number of strand',
    color_discrete_sequence=blue_shades
)

fig.update_traces(textposition='outside')

fig.update_layout(
    xaxis_title='School Type',
    yaxis_title='Number of Strand Offered',
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    showlegend=False
)

fig

#################################################################################

