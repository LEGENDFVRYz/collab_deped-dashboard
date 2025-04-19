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
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################




#################################################################################
##  --- Ratio enrollment in Academic vs. non-Academic tracks
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- Most and least enrolled  (strand)
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- Gender Distribution
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- Differences in the number of schools offering each track
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- Which SHS tracks are least offered but in high demand
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- How many schools offer each SHS track per region
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )
FILTERED_offerByRegion = dataframe = auto_extract(['strand', 'region', 'beis_id'], is_specific=True)
FILTERED_offerByRegion

strand_region_counts = FILTERED_offerByRegion.groupby(['strand', 'region'])['beis_id'].nunique().reset_index()


strand_region_counts.rename(columns={'beis_id': 'school_count'}, inplace=True)


fig = px.density_heatmap(
    strand_region_counts,
    x='region',
    y='strand',
    z='school_count',
    color_continuous_scale='Blues',
    title='Number of Schools Offering Each SHS Strand per Region',
    labels={'school_count': 'No. of Schools'}
)


fig.update_layout(
    xaxis_title='Region',
    yaxis_title='SHS Strand',
    yaxis=dict(autorange="reversed"),  # optional: puts strands in readable order
    margin=dict(l=60, r=40, t=60, b=60)
)

fig

#################################################################################



#################################################################################
##  --- Which SHS tracks are more prevalent in each sector
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )
FILTERED_byprevalent = dataframe = auto_extract(['strand', 'sector'], is_specific=True)
FILTERED_byprevalent

FILTERED_nostudents = dataframe = auto_extract(['counts'], is_specific=True)
FILTERED_nostudents

grade_enrollment2 = FILTERED_nostudents.groupby('grade')['counts'].sum().reset_index()
grade_enrollment2

merged = FILTERED_byprevalent.copy()
merged['counts'] = FILTERED_nostudents['counts']

grouped = merged.groupby(['strand', 'sector'])['counts'].sum().reset_index()

fig = px.bar(
    grouped,
    x='strand',
    y='counts',
    color='sector',
    barmode='group',
    title='Prevalence of SHS Strands by Sector (Based on Student Count)',
    labels={'strand': 'SHS Strand', 'counts': 'Number of Students', 'sector': 'School Sector'},
    color_discrete_sequence=px.colors.qualitative.Set2
)


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


fig = px.bar(
    track_counts,
    x='School Type',
    y='Number of strand',
    title='Number of SHS Strand Offered by Mother Schools vs Annexes',
    color='School Type',
    text='Number of strand'
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

