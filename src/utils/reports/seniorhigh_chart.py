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

mydf = auto_extract(['region', 'beis_id', 'track', 'strand'], is_specific=True)
grouped = mydf.groupby(['region', 'track'])['beis_id'].nunique().reset_index(name='school_count')
heatmap_data = grouped.pivot(index='region', columns='track', values='school_count').fillna(0)

fig = px.imshow(
    heatmap_data,
    labels=dict(x="SHS Track", y="Region", color="No. of Schools"),
    x=heatmap_data.columns,
    y=heatmap_data.index,
    color_continuous_scale="YlGnBu",
    text_auto=True
)

fig.update_layout(
    title="Number of Schools Offering Each SHS Track per Region",
    xaxis_title="SHS Track",
    yaxis_title="Region"
)
fig


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

