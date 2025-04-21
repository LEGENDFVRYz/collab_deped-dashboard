from random import sample
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
    Analytics/Location Charts and Indicator
    
"""


#################################################################################
##                     MAIN DATAFRAME BASED FROM THE QUERY                     ##
#################################################################################

# ## -- This only a temporary dataframe for testing your charts, you can change it
FILTERED_DF = dataframe = auto_extract(['counts','sector','region'], is_specific=False)
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

################################################################################
##  --- CHART: Student Enrollment by School Sector per Region
################################################################################
# 1. Automatically extract relevant columns
sector_df = auto_extract(['region', 'sector', 'counts'], is_specific=False)

# 2. Aggregate counts by region and sector, then sort so smaller sectors stack on top
sector_enrollment = (
    sector_df
    .groupby(['region', 'sector'])['counts']
    .sum()
    .reset_index()
)

# Sort within each region so that smaller sectors come first
sector_enrollment = (
    sector_enrollment
    .sort_values(['region', 'counts'], ascending=[True, True])
)

## 3. Define chronological region order (DepEd standard)
region_order = [
    'CAR', 'NCR', 'Region I', 'Region II', 'Region III', 'Region IV-A',
    'MIMAROPA', 'Region V', 'Region VI', 'Region VII', 'Region VIII',
    'Region IX', 'Region X', 'Region XI', 'Region XII', 'CARAGA', 'BARMM'
]

# Enforce this order on the data
sector_enrollment['region'] = pd.Categorical(
    sector_enrollment['region'],
    categories=region_order,
    ordered=True
)

# 4. Define exact sector order and assign red shades for sectors
sector_order  = ['Public', 'Private', 'SUCs/LUCs', 'PSO']
sector_colors = {
    'Public':    '#930F22',   # A darker red
    'Private':   '#E11C38',   # A mid red
    'SUCs/LUCs': '#FF5B72',   # A lighter red
    'PSO':       '#FF899A'    # A pinkish red
}


# 5. Build the stacked bar chart
sector_chart = px.bar(
    sector_enrollment,
    x='region',
    y='counts',
    color='sector',
    barmode='stack',
    category_orders={
        'region': region_order,
        'sector': sector_order
    },
    color_discrete_map=sector_colors,
    labels={
        'region': 'Region',
        'counts': 'Number of Students',
        'sector': 'School Sector'
    },
    title="Student Enrollment by School Sector per Region"
)

# 6. Uniform styling with y-axis tick formatting as "4M", "5M", etc.
sector_chart.update_layout(
    title_font=dict(size=20, family='Arial', color='#3C6382'),
    title_x=0.5,
    font=dict(family='Arial', size=14, color='#3C6382'),
    paper_bgcolor='#F0F0F0',
    plot_bgcolor='rgba(255,255,255,0.5)',
    margin=dict(l=50, r=30, t=70, b=60),
    legend=dict(
        title='School Sector',
        font=dict(size=14),
        x=1, y=1,
        xanchor='right', yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    xaxis=dict(showgrid=False, tickangle=-45),
    yaxis=dict(
        showgrid=False, 
        tickformat='.1s',  
        tickprefix='',     
        tickmode='auto'
    ),
    bargap=0.1
)

# 7. Add a bold white border to each segment
sector_chart.update_traces(
    marker_line_color='#FFFFFF',
    marker_line_width=2
)

# 8. Display the chart
sector_chart
#################################################################################



#################################################################################
##  --- CHART: Strand preferences per region
#################################################################################






#################################################################################



#################################################################################
##  --- INDICATOR: Total number of enrollees
#################################################################################






#################################################################################



#################################################################################
##  --- INDICATOR: Total number of schools
#################################################################################






#################################################################################



#################################################################################
##  --- TABLE: Total number of schools
#################################################################################






#################################################################################