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
    Analytics/Offering Charts and Indicator
    
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
# sample_chart.update_layout(
#     autosize=True,
#     margin={"l": 8, "r": 8, "t": 12, "b": 8},  # Optional: Adjust margins
# )
sample_chart

#################################################################################
#################################################################################




## -- FIND YOUR CHARTS HERE:

#################################################################################
##  --- CHART: Number of Schools by MCOC Type
#################################################################################






#################################################################################



#################################################################################
##  --- CHART: Gender Distribution Aross MCOC types
#################################################################################






#################################################################################



#################################################################################
##  --- CHART: MCOC Types Ranked by Total Student Enrollment
#################################################################################






#################################################################################



#################################################################################
##  --- CHART: Geographic Distribution of Program Offerings
#################################################################################






#################################################################################



#################################################################################
##  --- CHART: Enrollment Distribution by Grade Level
#################################################################################
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
# sample_chart.update_layout(
#     autosize=True,
#     margin={"l": 8, "r": 8, "t": 12, "b": 8},  # Optional: Adjust margins
# )
sample_chart
#################################################################################



#################################################################################
##  --- CHART: Number of MCOC Offerings per Location by School Level
#################################################################################






#################################################################################



#################################################################################
##  --- INDICATOR: Locations with the Highest and Lowest Number of Offerings
#################################################################################






#################################################################################



#################################################################################
##  --- INDICATOR: Total Number of Enrollees Across All MCOC Types
#################################################################################
FILTERED_Total = dataframe = auto_extract(['mod_coc','counts'], is_specific=True)
FILTERED_Total

grouped_by_MCOC= FILTERED_Total.groupby('mod_coc', as_index=False)['counts'].sum()
grouped_by_MCOC

total_All_Offering = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "All Offering", 'counts'].values[0]
total_All_Offering = (total_All_Offering)

total_ES_JHS = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "ES and JHS", 'counts'].values[0]
total_ES_JHS = (total_ES_JHS)

total_JHS_SHS = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "JHS with SHS", 'counts'].values[0]
total_JHS_SHS = (total_JHS_SHS)

total_Pure_ES = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "Purely ES", 'counts'].values[0]
total_Pure_ES = (total_Pure_ES)

total_Pure_JHS = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "Purely JHS", 'counts'].values[0]
total_Pure_JHS = (total_Pure_JHS)

total_Pure_SHS = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "Purely SHS", 'counts'].values[0]
total_Pure_SHS = (total_Pure_SHS)

mod_coc_categories = ["All Offering", "ES and JHS", "JHS with SHS", "Purely ES", "Purely JHS", "Purely SHS"]
counts = [total_All_Offering, total_ES_JHS, total_JHS_SHS, total_Pure_ES, total_Pure_JHS, total_Pure_SHS]

# Create table
fig = go.Figure(data=[go.Table(
    header=dict(values=["<b>mod_coc</b>", "<b>Counts</b>"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[mod_coc_categories, counts],
               fill_color='lavender',
               align='left'))
])

fig.update_layout(title_text="Summary of Counts by mod_coc Category")
fig

#################################################################################