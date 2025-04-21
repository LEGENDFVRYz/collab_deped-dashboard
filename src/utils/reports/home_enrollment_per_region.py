import re, os, sys
from turtle import title
import dash, math
from dash import dcc, html

import numpy as np
from numpy import average
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from config import project_root
from utils.get_data import auto_extract

# ----------------------------------------------------------
# Number Format

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

## -- INDICATORS: Total Enrollees
def format_large_number(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)

#################################################################################
##                     MAIN DATAFRAME BASED FROM THE QUERY                     ##
#################################################################################

# -- Create the appropriate plot
dataframe = auto_extract(['counts'], is_specific=False)

order = [
    'K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'ES NG', 'G7', 'G8', 'G9', 'G10', 'JHS NG', 'G11', 'G12'
]

dataframe['school-level'] = dataframe['grade'].apply(
    lambda x: 'JHS' if x in ['G7', 'G8', 'G9', 'G10', 'JHS NG'] else ('SHS' if x in ['G11', 'G12'] else 'ELEM')
)
dataframe

query = dataframe.groupby(['school-level','grade'], as_index=False)[['counts']].sum()

query['grade'] = pd.Categorical(query['grade'], categories=order, ordered=True)
query = query.sort_values('grade')
query['formatted_counts'] = query['counts'].apply(smart_truncate_number)

# print(dataframe.columns)

# Ploting
home_enrollment_per_region = px.bar(query, 
                                    x="counts", 
                                    y="grade",
                                    text="formatted_counts",
                                    orientation='h',
                                    custom_data=['school-level'],
                                    color='school-level',
                                    color_discrete_map={
                                        'ELEM': '#037DEE', 
                                        'JHS': '#FE4761', 
                                        'SHS': '#FFBF5F'    
                                    }
                            )
home_enrollment_per_region

# Layout configs
home_enrollment_per_region.update_traces(
    textposition='outside',
    cliponaxis=False,
    textfont=dict(size=8, color="#04508c"),
    hovertemplate='Education Level: %{customdata[0]}<br>Enrollees: %{x}<br>Grade-level: %{y}',
)
home_enrollment_per_region.update_layout(yaxis=dict(visible=True), xaxis=dict(visible=False))
home_enrollment_per_region.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 8, "b": 8},  # Optional: Adjust margins
    paper_bgcolor='rgba(0, 0, 0, 0)', 
    plot_bgcolor='rgba(0, 0, 0, 0)',
    yaxis=dict(
        automargin=True,
        showticklabels=True,
        title=None,
        tickfont=dict(size=9, color="#9DADBD"),
        ticksuffix = "  "
    ),
    xaxis=dict(
        automargin=True,
        title=None,
        categoryorder='array',
        categoryarray=order,
    ),
    legend=dict(
        title=None,
        orientation="h",  # Horizontal legend
        yanchor="bottom",  # Align legend at the bottom
        y=1.025,  # Position it below the chart
        xanchor="center",  # Center it horizontally
        x=0.45  # Align it to the center
    )
)

# ----------------------------------------------------------
shs_df = auto_extract(['strand', 'track', 'shs_grade', 'counts'], is_specific=False)
shs_df

es_count = dataframe[dataframe['school-level'] == 'ELEM']['counts'].sum()
jhs_count = dataframe[dataframe['school-level'] == 'JHS']['counts'].sum()
shs_count = dataframe[dataframe['school-level'] == 'SHS']['counts'].sum()

total_enrollees = es_count + jhs_count + shs_count
total_enrollees

total_enrollees_formatted = smart_truncate_number(total_enrollees)
total_enrollees_formatted

## -- INDICATORS: Most and Least active school level
most_active =   query.loc[query['counts'].idxmax()]
least_active =  query.loc[query['counts'].idxmin()]



## -- INDICATORS: Total Enrollees
count_shs_school = shs_df['beis_id'].nunique()
total_shs_enrollees = shs_df['counts'].sum()
total_shs_enrollees


# # Ratio per Strand
# total_enrollees_per_strand = shs_df.groupby('strand', as_index=False)['counts'].sum()
# total_enrollees_per_strand['ratio'] = total_enrollees_per_strand['counts'] / total_shs_enrollees
# total_enrollees_per_strand

# academic_track_ratio = total_enrollees_per_strand[total_enrollees_per_strand['track'] == 'ACAD'].values.tolist()[0][2]

# # Ratio per track
# total_enrollees_per_track = shs_df[
#                                 shs_df['strand'] == 'ACAD'
#                             ].groupby('track', as_index=False)['counts'].sum()
# total_enrollees_per_track['ratio'] = total_enrollees_per_track['counts'] / total_shs_enrollees
# total_enrollees_per_track

# filtered_non_acad = total_enrollees_per_strand[total_enrollees_per_strand['strand'] == 'NON ACAD'].values.tolist()[0]
# total_enrollees_per_track.loc[len(total_enrollees_per_track)] = pd.Series(filtered_non_acad, index=total_enrollees_per_track.columns)
# total_enrollees_per_track


# avg_stem = shs_df[shs_df['track'] == 'STEM']['counts'].sum() / total_shs_enrollees
# avg_stem

# average_per_track = shs_df['track'].value_counts(normalize=True)
# average_per_track

# # Ploting
# custom_colors = ['#00AD7F', '#E0E0E0']
# explode = [0, 0.15]

# track_ratio_per_track = go.Figure(
#     data=[
#         go.Pie(labels=total_enrollees_per_strand['strand'], 
#                values=total_enrollees_per_strand['ratio'], 
#                marker=dict(colors=custom_colors),
#                pull=explode
#     )]
# )

# # Layout configs
# track_ratio_per_track.update_layout(
#     autosize=True,
#     margin={"l": 8, "r": 8, "t": 16, "b": 0},  # Optional: Adjust margins
# )

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
             )

home_school_number_per_sector.update_traces(textposition="outside", marker_color="#037DEE")
home_school_number_per_sector.update_layout(yaxis=dict(visible=False), xaxis=dict(visible=False))
home_school_number_per_sector.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 16, "b": 8},  # Optional: Adjust margins
    paper_bgcolor='rgba(0, 0, 0, 0)', 
    plot_bgcolor='rgba(0, 0, 0, 0)',   
    yaxis=dict(showticklabels=True),
)

home_school_number_per_sector

# ----------------------------------------------------------
# Gender Distribution

grouped_by_gender = dataframe.groupby(['gender'], as_index=False)['counts'].sum()

colors = ['#FF5B72', '#5DB7FF']

# Create half-donut chart
home_gender_distribution = go.Figure(go.Pie(
    labels=grouped_by_gender['gender'],
    values=grouped_by_gender['counts'],
    hole=0.70,
    direction='clockwise',
    sort=False,
    # textinfo='percent', 
    # textposition='inside', 
    # insidetextorientation='horizontal', 
    textfont=dict(size=12, color='black'),
    # textinfo='label+percent',
    marker=dict(colors=colors)
))

home_gender_distribution.update_layout(
    showlegend=False,
    margin=dict(t=0, b=0, l=0, r=0),
    annotations=[dict(text='Gender<br>Distribution',
                      x=0.5,
                      y=0.5,
                      font=dict(color='#3C6382', size=15),
                      align='center',
                      showarrow=False)],
)

home_gender_distribution.update_traces(rotation=180)
home_gender_distribution

total_male_count = grouped_by_gender.loc[grouped_by_gender['gender'] == 'M', 'counts'].values[0]
total_male_count_formatted = smart_truncate_number(total_male_count)

total_female_count = grouped_by_gender.loc[grouped_by_gender['gender'] == 'F', 'counts'].values[0]
total_female_count_formatted = smart_truncate_number(total_female_count)

if total_male_count > total_female_count:
    gender_gap = ((total_male_count - total_female_count) / total_female_count) * 100
    greater_gender = "MALE"
    lesser_gender = "FEMALE"
elif total_female_count > total_male_count:
    gender_gap = ((total_female_count - total_male_count) / total_male_count) * 100
    greater_gender = "FEMALE"
    lesser_gender = "MALE"
else:
    gender_gap = 0

gender_gap = round(gender_gap, 2)

# ----------------------------------------------------------
# Regional Distribution

enrollees_df = auto_extract(['counts', 'region'], is_specific=False)
enrollees_df

enrollees_per_region = enrollees_df.groupby(['region'], as_index=False)["counts"].sum()
enrollees_per_region["counts_label"] = enrollees_per_region["counts"].apply(smart_truncate_number)

ordered_regions = [
    'Region I', 'Region II', 'Region III', 'Region IV-A', 'Region IV-B',
    'Region V', 'Region VI', 'Region VII', 'Region VIII', 'Region IX',
    'Region X', 'Region XI', 'Region XII', 'CAR', 'NCR', 'CARAGA',
    'BARMM', 'PSO'
]

enrollees_per_region['region'] = pd.Categorical(
    enrollees_per_region['region'],
    categories=ordered_regions,
    ordered=True
)

enrollees_per_region = enrollees_per_region.sort_values('region').reset_index(drop=True)
enrollees_per_region

home_regional_distribution = px.bar (enrollees_per_region, x="region", y="counts", 
                                text="counts_label"
                            )

home_regional_distribution.update_traces(
    marker_color="#037DEE",
    textposition='outside',
    cliponaxis=False,
    textfont=dict(size=8, color="#04508c"),
    hovertemplate='Region: %{x}<br>Enrollees: %{y}',
    # hovertext=enrollees_per_region['counts'].astype(str)
)

home_regional_distribution.update_layout(
    autosize=True,
    margin={"l": 8, "r": 8, "t": 8, "b": 8},
    plot_bgcolor='#ECF8FF',         
    yaxis=dict(
        automargin=True,
        title=None,
        showgrid=True,            
        gridcolor='#D2EBFF',          
        zeroline=False,
        tickfont=dict(size=8, color="#9DADBD")             
    ),
    xaxis=dict(
        automargin=True,
        title=None,
        tickangle=-45,
        tickfont=dict(size=8, color="#9DADBD")
    ),
    # transition=dict(duration=20000, easing="cubic-in-out"),
)

home_regional_distribution


# ----------------------------------------------------------
# Total Number of Schools Available

number_of_schools = df4["beis_id"].count()
number_of_schools_formatted = smart_truncate_number(number_of_schools)

# ----------------------------------------------------------
# Enrollees per Education Level

grouped_by_school_level = dataframe.groupby('school-level', as_index=False)['counts'].sum()

total_es_count = grouped_by_school_level.loc[grouped_by_school_level["school-level"] == "ELEM", 'counts'].values[0]
total_es_count_formatted = smart_truncate_number(total_es_count)

total_jhs_count = grouped_by_school_level.loc[grouped_by_school_level["school-level"] == "JHS", 'counts'].values[0]
total_jhs_count_formatted = smart_truncate_number(total_jhs_count)

total_shs_count = grouped_by_school_level.loc[grouped_by_school_level["school-level"] == "SHS", 'counts'].values[0]
total_shs_count_formatted = smart_truncate_number(total_shs_count)

# ----------------------------------------------------------
# Schools Count per Subclassification

# Subclassification School Count - Chart
subclass_extract = auto_extract(['counts', 'sub_class'], is_specific=False)

subclass_df1 = (
    subclass_extract.groupby('sub_class')
    .agg(
        school_count=('beis_id', 'nunique'),
        counts=('counts', 'sum'),  
    )
    .reset_index()
)

home_subclass_chart = px.bar(
    subclass_df1,
    x='school_count',           # Number of schools
    y='sub_class',              # Subclassification
    orientation='h',            # Horizontal bars
    text='school_count',        # Show school count as text
    color='sub_class',          # Optional: add color by sub_class
    color_discrete_sequence=px.colors.qualitative.Set2  # Nice color palette
)

home_subclass_chart.update_traces(
    textposition='outside',     # Show text outside bars
    marker_line_width=0.5,      # Add outline to bars
    marker_line_color='gray'
)

home_subclass_chart.update_layout(
    title='Number of Schools per Subclassification',
    xaxis_title='Number of Schools',
    yaxis_title=None,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=80, r=20, t=50, b=20),
    yaxis=dict(
        tickfont=dict(size=10, color='#4A4A4A')
    ),
    xaxis=dict(
        tickfont=dict(size=10, color='#4A4A4A'),
        gridcolor='#EDEDED',
        showgrid=True,
        zeroline=False
    ),
    showlegend=False
)

home_subclass_chart

# Subclassification School Count - Table
home_subclass_table = go.Figure(data=[go.Table(
    header=dict(
        values=["<b>Subclassification</b>", "<b>School Count</b>", "<b>Student Count</b>"],
        fill_color='rgba(0,0,0,0)',  # Transparent header background
        font=dict(color='black', size=12),
        line_color='rgba(0,0,0,0)',  # Hide header borders
        align='left',
    ),
    cells=dict(
        values=[
            subclass_df1['sub_class'],
            subclass_df1['school_count'],
            subclass_df1['counts']
        ],
        fill_color='rgba(0,0,0,0)',  # Transparent cell background
        font=dict(color='black', size=11),
        line_color='rgba(0,0,0,0)',  # Hide cell borders
        align='left'
    )
)])

# Layout settings
home_subclass_table.update_layout(
    autosize=True,
    margin=dict(l=10, r=10, t=0, b=10),
    paper_bgcolor='rgba(0,0,0,0)',  # Fully transparent background
    plot_bgcolor='rgba(0,0,0,0)',
)

home_subclass_table

# ----------------------------------------------------------
# Ratio of Schools by Program Offering

# Extract and group
program_offering_extract = auto_extract(['mod_coc'], is_specific=False)
grouped_by_offering = program_offering_extract.groupby("mod_coc").size().reset_index(name="counts")

# Flags for outer donut totals
grouped_by_offering['has_ES'] = grouped_by_offering['mod_coc'].str.contains('ES', case=False, na=False) | \
                                grouped_by_offering['mod_coc'].str.contains('All Offering', case=False, na=False)
grouped_by_offering['has_JHS'] = grouped_by_offering['mod_coc'].str.contains('JHS', case=False, na=False) | \
                                grouped_by_offering['mod_coc'].str.contains('All Offering', case=False, na=False)
grouped_by_offering['has_SHS'] = grouped_by_offering['mod_coc'].str.contains('SHS', case=False, na=False) | \
                                grouped_by_offering['mod_coc'].str.contains('All Offering', case=False, na=False)

# Program totals
es_total = grouped_by_offering.loc[grouped_by_offering['has_ES'], 'counts'].sum()
jhs_total = grouped_by_offering.loc[grouped_by_offering['has_JHS'], 'counts'].sum()
shs_total = grouped_by_offering.loc[grouped_by_offering['has_SHS'], 'counts'].sum()

# Outer donut (Programs)
program_totals = pd.DataFrame({
    'program': ['ES', 'JHS', 'SHS'],
    'total_count': [es_total, jhs_total, shs_total]
})

outer_labels = program_totals['program']
outer_values = program_totals['total_count']
outer_color_map = {
    'ES': '#037DEE',
    'JHS': '#FE4761',
    'SHS': '#FFBF5F'
}

outer_colors = outer_labels.map(outer_color_map)

# Inner donut (Offerings) with gradient sort
desired_order = [
    'Purely ES',
    'Purely JHS',
    'Purely SHS',
    'ES and JHS',
    'JHS with SHS',
    'All Offering'
]
inner_color_map = {
    'Purely ES': '#002242',
    'Purely JHS': '#004386',
    'Purely SHS': '#0162C2',
    'ES and JHS': '#5EAFFF',
    'JHS with SHS': '#ADDBFF',
    'All Offering': '#E2F2FF'
}

# Apply desired order
grouped_by_offering['mod_coc'] = pd.Categorical(
    grouped_by_offering['mod_coc'],
    categories=desired_order,
    ordered=True
)
grouped_by_offering = grouped_by_offering.sort_values('mod_coc')

inner_labels = grouped_by_offering['mod_coc']
inner_values = grouped_by_offering['counts']
inner_colors = inner_labels.map(inner_color_map)

# Create donut chart
home_program_offering = go.Figure()

# Outer donut
home_program_offering.add_trace(go.Pie(
    labels=outer_labels,
    values=outer_values,
    hole=0.7,
    direction='clockwise',
    sort=False,
    textinfo='none',
    textposition='inside',
    marker=dict(colors=outer_colors, line=dict(color='#3C6382', width=0)),
    domain={'x': [0, 1], 'y': [0, 1]},
    name='Programs',
    legendgroup='Program Offering',
    showlegend=True
))

# Inner donut
home_program_offering.add_trace(go.Pie(
    labels=inner_labels,
    values=inner_values,
    hole=0.43,
    direction='clockwise',
    rotation=90,
    sort=False,
    textinfo='none',
    textposition='inside',
    marker=dict(colors=inner_colors, line=dict(color='#3C6382', width=0)),
    domain={'x': [0.2, 0.8], 'y': [0.2, 0.8]},
    name='Level',
    legendgroup='Education Level',
    showlegend=True
))

# Layout
home_program_offering.update_layout(
    showlegend=True,
    autosize=True,
    margin=dict(t=20, b=20, l=20, r=20),
    # annotations=[dict(
    #     text='Programs<br>& Offerings',
    #     x=0.5, y=0.5, font_size=14, showarrow=False, font=dict(color='#3C6382')
    # )],
    legend=dict(
        # orientation='h',
        # yanchor='top',
        # y=-0.1,
        # xanchor='center',
        # x=0.5,
        orientation='v',       # vertical layout
        yanchor='middle',      # anchor at the middle vertically
        y=0.5,                 # center of the y-axis
        xanchor='left',        # anchor the x at the left of the legend box
        x=1.05,  
    )
)

# Show the chart
home_program_offering

# ----------------------------------------------------------
# Senior High School Tracks Distribution

shs_tracks_df = auto_extract(['track'], is_specific=False)
grouped_by_tracks = shs_tracks_df.groupby(["track"], as_index=False)["counts"].sum()

home_shs_tracks = px.bar(
    grouped_by_tracks,
    x="track",
    y="counts",
)

home_shs_tracks.update_layout(
    autosize=True,
    margin=dict(t=10, b=10, l=10, r=10),
)

home_shs_tracks