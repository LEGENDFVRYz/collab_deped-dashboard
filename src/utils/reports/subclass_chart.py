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
FILTERED_DF = dataframe = auto_extract(['counts','sub_class'], is_specific=False)

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

FILTERED_DF['sub_class'] = FILTERED_DF['sub_class'].map(subclass_rename).fillna(FILTERED_DF['sub_class'])
FILTERED_DF['type'] = FILTERED_DF['type'].map(type_rename).fillna(FILTERED_DF['type'])
FILTERED_DF['sector'] = FILTERED_DF['sector'].map(sector_rename).fillna(FILTERED_DF['sector'])

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
    margin={"l": 8, "r": 8, "t": 8, "b": 8},
)



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
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- MCOC breakdown/which subclass offers which program types
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- Enrollment in shs tracks across subclass
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- % schools offering ‘all offerings’ per subclass
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################



#################################################################################
##  --- % schools offering shs per subclass
#################################################################################
# dist_per_track_chart = px.bar(filtered_df, )





#################################################################################