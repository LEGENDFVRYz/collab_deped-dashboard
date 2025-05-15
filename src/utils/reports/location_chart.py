from enum import auto
from turtle import title, width
from unicodedata import category
import numpy as np
import pandas as pd
import dash
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, callback, Output, Input, State, Patch
from plotly.subplots import make_subplots 

import json
from pathlib import Path
import re, os, sys
import plotly.express as px
from geojson_rewind import rewind
import pandas as pd
import plotly.io as pio 
from rapidfuzz import process, fuzz
import unicodedata
import re
    
# important part
from src.data import enrollment_db_engine, smart_filter

# Extra Utilities
from src.utils.extras_utils import smart_truncate_number

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import project_root


"""
    Analytics/Location Charts and Indicator
    
"""


#################################################################################
##                     MAIN DATAFRAME BASED FROM THE QUERY                     ##
#################################################################################

# # ## -- This only a temporary dataframe for testing your charts, you can change it whatever you want

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# from config import project_root
# from utils.get_data import auto_extract

# FILTERED_DF = dataframe = auto_extract(['counts'], is_specific=False)
# FILTERED_DF

# ## -- Check the document for all valid columns and structurette
# ## -- Dont change the all caps variables

#################################################################################

# ## QUERYY
# @callback(
#     Output('base-trigger', 'data'),
#     Output('render-base', 'children'),
#     Input("url", "pathname"),
#     State('base-trigger', 'data')
# )
# def trigger_base_charts(pathname, base_status):
#     if pathname != "/analytics":
#         return dash.no_update, html.Div([])
    
#     # Initialize DF
#     smart_filter({}, _engine=enrollment_db_engine)
    
#     return (not base_status), dash.no_update





## -- FIND YOUR CHARTS HERE:

################################################################################
##  --- CHART: Distribution of enrollees per location 
#################################################################################

@callback(
    Output('location_enrollees-distribution-per-location', 'children'),
    Output('edrg-graph-title', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    FILTERED_DATA = FILTERED_DATA[['beis_id', 'brgy', 'municipality', 'district', 'division', 'province', 'region', 'counts', 'gender']]
    # print("triggered dispilinr")
    
    ## LOCATION SCOPE
    locs = ['beis_id', 'brgy', 'municipality', 'district', 'division', 'province', 'region']
    tag = "default"
    min_loc = 6

    for i, loc in enumerate(locs[1:]):
        if loc in data:
            min_loc = i
            break

    loc_scope = locs[min_loc]
    
    
    ## TITLE
    # try:
    #     values = data.get(locs[min_loc + 1], [])
    #     if len(values) > 1:
    #         tag = ["Distribution Breakdown for the ", html.Span(["Chosen Location"], className="lfury-highlight"),]
    #     else:
    #         tag = ["Distribution Breakdown by ", html.Span([f"{loc_scope.capitalize()} of {values[0]}"], className="lfury-highlight")]
    # except (IndexError, KeyError, TypeError):
    #     tag = ["Distribution Breakdown by ", html.Span([f"{loc_scope.capitalize()} of {values[0]}"], className="lfury-highlight")]
    
    try:
        values = data.get(locs[min_loc + 1], [])
        if len(values) > 1:
            tag = [
                "Distribution Breakdown for the ",
                html.Span([" Chosen Location "], className="lfury-highlight"),
            ]
        else:
            tag = [
                "Distribution Breakdown by ",
                html.Span([f" {loc_scope.capitalize()} of {values[0]} "], className="lfury-highlight"),
            ]
    except (IndexError, KeyError, TypeError):
        # Fall back to a default string or empty value
        tag = [
            "Distribution Breakdown by ",
            html.Span([f" {loc_scope.capitalize()} of Philippines "], className="lfury-highlight"),
        ]
    
    # Step 1: Group by region and gender
    total_counts = FILTERED_DATA.groupby(loc_scope, observed=True)['counts'].sum().reset_index()
    total_counts = total_counts.sort_values(by='counts', ascending=True)

    # Step 2: Group by region and gender, and calculate counts
    gender_region = FILTERED_DATA.groupby([loc_scope, 'gender'], observed=True)['counts'].sum().reset_index()

    # Step 3: Ensure that the 'loc_scope' in gender_region has the same ordering as in total_counts
    gender_region[loc_scope] = pd.Categorical(
        gender_region[loc_scope], 
        categories=total_counts[loc_scope].tolist(), 
        ordered=True
    )
    
    # Step 4: Optionally, sort gender_region based on the ordered loc_scope categories
    gender_region = gender_region.sort_values(by=loc_scope)
    
    # Step 2: Define brand colors
    brand_colors = {
        'M': '#5DB7FF',
        # 'F': '#FF5B72',
        'F': '#e11c38',
    }

    # Step 3: Create the stacked bar chart
    gender_region_fig = px.bar(
        gender_region,
        x='counts',
        y=loc_scope,
        color='gender',
        orientation='h',
        barmode='stack',
        labels={
            'counts': 'Number of Enrollees',
            # Removed 'region' label to prevent it from auto-setting y-axis title
            'gender': 'Gender'
        },
        color_discrete_map=brand_colors
    )
    
    # Step 4: Calculate total per region for annotations
    region_totals = gender_region.groupby(loc_scope, observed=True)['counts'].sum().reset_index()

    # Step 5: Add truncated total annotations
    for _, row in region_totals.iterrows():
        short_text = smart_truncate_number(row['counts'])  # Your truncation logic
        gender_region_fig.add_annotation(
            x=row['counts'] + 1,
            y=row[loc_scope],
            text=short_text,
            hovertext=str(row['counts']),
            showarrow=False,
            font=dict(color="#667889", family='Inter Bold'),
            xanchor="left",
            yanchor="middle",
        )

    # Step 6: Customize layout (explicitly clear y-axis title)
    gender_region_fig.update_layout(
        yaxis=dict(
            automargin=True,
            title=None,
            ticksuffix="   "
        ),
        xaxis=dict(
            showline=True,
            linecolor='black',   # or any visible color like '#667889'
            linewidth=1          # optional, default is 1
        ),
        legend=dict(
            orientation="h",       # horizontal layout
            yanchor="top",         # anchor from top of legend box
            y=-0.15,                # position legend below x-axis label
            xanchor="center",      # center the legend horizontally
            x=0.5,                 # center relative to plot width
        ),
        xaxis_title="Number of Students",
        yaxis_title="",  # Remove the default "Region" title
        legend_title="Gender",
        # tickpadding=10,
        font=dict(color="#667889", family='Inter'),
        margin=dict(l=0, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        barcornerradius=6,
    )

    return dcc.Graph(figure=gender_region_fig), tag

#################################################################################




# #################################################################################
# ##  --- CHART: enrollment density (students per location)
# #################################################################################

# #################################################################################



# #################################################################################
# ##  --- CHART: school sectors
# #################################################################################

@callback(
    Output('location_school_sectors', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    locs = ['brgy', 'municipality', 'district', 'division', 'province', 'region']

    min_loc = 5

    for i, loc in enumerate(locs[1:]):
        if loc in data:
            min_loc = i
            break

    loc_scope = locs[min_loc]
    
    
    
    sector_enrollment = (
        FILTERED_DATA
        .groupby([loc_scope, 'sector'], observed=True)['counts']
        .sum()
        .reset_index()
    )

    sector_enrollment = (
        sector_enrollment
        .sort_values([loc_scope, 'counts'], ascending=[True, True])
    )

    # region_order = [
    #     'CAR', 'NCR', 'Region I', 'Region II', 'Region III', 'Region IV-A',
    #     'Region IV-B', 'Region V', 'Region VI', 'Region VII', 'Region VIII',
    #     'Region IX', 'Region X', 'Region XI', 'Region XII', 'CARAGA', 'BARMM'
    # ]

    # sector_enrollment['region'] = pd.Categorical(
    #     sector_enrollment['region'],
    #     categories=region_order,
    #     ordered=True
    # )

    sector_order  = ['Public', 'Private', 'SUCs/LUCs', 'PSO']
    sector_colors = {
        'Public':    '#930F22',
        'Private':   '#E11C38',  
        'SUCs/LUCs': '#FF5B72',  
        'PSO':       '#FF899A'   
    }

    sector_enrollment['sector'] = pd.Categorical(
        sector_enrollment['sector'],
        categories=sector_order,
        ordered=True
    )

    sector_chart = px.bar(
        sector_enrollment,
        x=loc_scope,
        y='counts',
        color='sector',
        barmode='stack',
        category_orders={
            # 'region': region_order,
            'sector': sector_order
        },
        color_discrete_map=sector_colors,
        labels={
            loc_scope: loc_scope.capitalize(),
            'counts': 'Number of Students',
            'sector': 'School Sector',
        },
    )

    sector_chart.update_layout(
        autosize=True,
        title=None,  # Remove the main chart title
        font=dict(family='Inter, sans-serif', size=14, color='#3C6382'),
        plot_bgcolor='rgba(255,255,255,0.5)',
        margin=dict(l=50, r=30, t=70, b=60),
        legend=dict(
            title=None,
            orientation='h',
            yanchor='bottom',
            y=-0.9,
            xanchor='center',
            x=0.5,
            font=dict(size=14),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        ),
        xaxis=dict(
            title=None,         # Remove x-axis title
            showgrid=False,
            tickangle=-45
        ),
        yaxis=dict(
            title=None,         # Remove y-axis title
            showgrid=False,
            tickformat='.1s',
            tickprefix=''
        ),
        bargap=0.1
    )

    sector_chart.update_traces(
        marker_line_color='#FFFFFF',
        marker_line_width=2
    )

    return dcc.Graph(figure=sector_chart)

# #################################################################################



# #################################################################################
# ##  --- CHART: school sectors
# #################################################################################






# #################################################################################



# #################################################################################
# ##  --- CHART: Strand preferences per region
# #################################################################################
@callback(
    Output('track-preference-heatmap', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    locs = ['brgy', 'municipality', 'district', 'division', 'province', 'region']

    min_loc = 5

    for i, loc in enumerate(locs[1:]):
        if loc in data:
            min_loc = i
            break

    loc_scope = locs[min_loc]
    
    # Cleaning
    clean_df = FILTERED_DATA[FILTERED_DATA['grade'].isin(['G11', 'G12'])].copy()
    # clean_df['track'] = clean_df['track'].cat.remove_unused_categories()
    clean_df['track'] = clean_df['track'].cat.remove_unused_categories()
    
    # Step 2: Group and SUM the 'counts' for track-level heatmap
    track_data = clean_df.groupby([loc_scope, 'track'], observed=True)['counts'].sum().reset_index()
    track_pivot = track_data.pivot(index='track', columns=loc_scope, values='counts').fillna(0)

    # Step 3: Group and SUM the 'counts' for strand-level heatmap
    clean_df = clean_df[clean_df['strand'] != '__NaN__']
    clean_df['strand'] = clean_df['strand'].cat.remove_unused_categories()
    strand_data = clean_df.groupby([loc_scope, 'strand'], observed=True)['counts'].sum().reset_index()
    strand_pivot = strand_data.pivot(index='strand', columns=loc_scope, values='counts').fillna(0)
    
    # Step 4: Create subplots
    heatmap_fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03
    )

    # Heatmap for Track
    heatmap_fig.add_trace(
        go.Heatmap(
            z=track_pivot.values,
            x=track_pivot.columns.tolist(),
            y=track_pivot.index.tolist(),
            colorscale=[
                "#074889", "#0C6DC1", "#1389F0", "#00CCFF", 
                "#00F2FF", "#89FE2A", "#F9F521", "#FFB700"
            ],
            # colorbar=dict(title="Students Enrolled")
        ),
        row=1, col=1
    )

    # Heatmap for Strand
    heatmap_fig.add_trace(
        go.Heatmap(
            z=strand_pivot.values,
            x=strand_pivot.columns.tolist(),
            y=strand_pivot.index.tolist(),
            colorscale=[
                "#074889", "#0C6DC1", "#1389F0", "#00CCFF", 
                "#00F2FF", "#89FE2A", "#F9F521", "#FFB700"
            ],
            showscale=False  # Only show one colorbar
        ),
        row=2, col=1
    )

    # Step 5: Update layout
    heatmap_fig.update_layout(
        height=400,
        width=600,
        title_text=None,
        xaxis2=dict(title=None, tickangle=45),
        yaxis=dict(title=None),
        yaxis2=dict(title=None),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return dcc.Graph(figure=heatmap_fig)

# #################################################################################



# #################################################################################
# ##  --- INDICATOR: Total number of enrollees
# #################################################################################

@callback(
    Output('raw-average-enrollees', 'children'),
    Output('truncated-average-enrollees', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    locs = ['brgy', 'municipality', 'district', 'division', 'province', 'region']

    min_loc = 5

    for i, loc in enumerate(locs[1:]):
        if loc in data:
            min_loc = i
            break

    loc_scope = locs[min_loc]
    
    FILTERED_DATA = FILTERED_DATA[[loc_scope, 'counts']]
    df_grouped = FILTERED_DATA.groupby(loc_scope, as_index=False, observed=True)['counts'].sum()

    # Median enrollees per school
    median_enrollees_per_school = int(df_grouped['counts'].median())
    
    truncated_total_enrollees = smart_truncate_number(median_enrollees_per_school)

    return f"{median_enrollees_per_school:,} average enrollees", truncated_total_enrollees




@callback(
    Output('raw-total-enrollees', 'children'),
    Output('truncated-total-enrollees', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    raw_total_enrollees = FILTERED_DATA['counts'].sum()
    truncated_total_enrollees = smart_truncate_number(raw_total_enrollees)

    # # get the median
    # median_enrolless = FILTERED_DATA['counts'].median()
    
    # # Filter and compute ratio of enrollees below the median
    # below_median_sum = FILTERED_DATA[FILTERED_DATA['counts'] < median_enrolless]['counts'].sum()

    # # Ratio of enrollees below 50%
    # ratio_below_50 = below_median_sum / raw_total_enrollees if raw_total_enrollees > 0 else 0
        
    raw_total_enrollees
    truncated_total_enrollees
    
    return f"{raw_total_enrollees:,} enrollees", truncated_total_enrollees

# #################################################################################



# #################################################################################
# ##  --- INDICATOR: Total number of schools
# #################################################################################

@callback(
    Output('raw-total-schools', 'children'),
    Output('truncated-total-schools', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    # Count total number of unique schools
    raw_total_schools = FILTERED_DATA['name'].nunique()
    truncated_total_schools = smart_truncate_number(raw_total_schools)

    raw_total_schools
    truncated_total_schools
    
    return f"{raw_total_schools:,} schools", truncated_total_schools

# #################################################################################



# #################################################################################
# ##  --- TABLE: Total number of schools
# #################################################################################

@callback(
    Output('location_highest_lowest_enrollees', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    # Step 1: Group by school and region, summing the counts
    aggregated_df = FILTERED_DATA.groupby(['name', 'region'], as_index=False)['counts'].sum()

    
    # --- INSERT THIS to filter out schools with 0 enrollees ---
    aggregated_df = aggregated_df[aggregated_df['counts'] > 0]

    
    # Step 2: Get the school with highest and lowest total enrollees
    max_row = aggregated_df.loc[aggregated_df['counts'].idxmax()]
    min_row = aggregated_df.loc[aggregated_df['counts'].idxmin()]

    # Step 3: Combine them into a new DataFrame for visualization
    highest_lowest2 = pd.DataFrame([max_row, min_row])

    hi_low_fig = go.Figure(data=[go.Table(
        columnorder=[1, 2, 3],
        columnwidth=[80, 40, 50],

        header=dict(
            values=["School Name", "Region", "Total Enrollees"],
            fill_color='#E6F2FB',
            align='left',
            font=dict(family='Inter', color='#04508c', size=12),
            line_color='#B0C4DE',
            height=40  # header height
        ),
        cells=dict(
            values=[
                highest_lowest2['name'].apply(lambda x: f"{x}\n"),
                highest_lowest2['region'],
                highest_lowest2['counts']
            ],
            fill_color=['#FFFFFF', '#F7FAFC'],
            align='left',
            font=dict(family='Inter', color='#3C6382', size=12),
            line_color='#D3D3D3',
            height=90  # fixed cell height
        )
    )])

    hi_low_fig.update_layout(
        # autosize=True, 
        height=220,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    return dcc.Graph(
        figure=hi_low_fig,
        config={
            "responsive": True,
            # "staticPlot": True  # disables zoom, pan, hover, etc.
        },
        style={
            "width": "100%",
            # "height": "200px",     # fixed height to prevent overflow
            # "overflow": "hidden"   # ensure no scroll
        }
    )

# #################################################################################


@callback(
    Output('enrollment-by-years', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    
    df = FILTERED_DATA[['brgy', 'municipality', 'district', 'division', 'province', 'region', 'counts', 'year']]
    
    locs = ['brgy', 'municipality', 'district', 'division', 'province', 'region']
    min_loc = 5

    for i, loc in enumerate(locs[1:]):
        if loc in data:
            min_loc = i
            break

    loc_scope = locs[min_loc]

    df['year'] = df['year'].astype(str)
    df_grouped = df.groupby([loc_scope, 'year'], as_index=False)['counts'].sum()

    sorted_regions = sorted(df_grouped[loc_scope].unique())
    df_grouped[loc_scope] = pd.Categorical(df_grouped[loc_scope], categories=sorted_regions, ordered=True)
    df_grouped = df_grouped.sort_values(by=[loc_scope, 'year'])

    changes_chart = px.line(
        df_grouped,
        x='year',
        y='counts',
        color=loc_scope,
        markers=True
    )

    changes_chart.update_layout(
        title=None,
        xaxis_title="Year",
        yaxis_title=None,
        xaxis=dict(type='category'),
        margin=dict(t=20, b=20),
    )

    return dcc.Graph(
        figure=changes_chart,
        config={"responsive": True},
        style={"width": "100%", "marginBottom": "10px"}
    )


@callback(
    Output('total-enrollment-by-year', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    
    df = FILTERED_DATA[['region', 'counts', 'year']]
    national_enrollment = df.groupby('year', as_index=False)['counts'].sum()

    enrollment_bar = px.bar(
        national_enrollment,
        x='year',
        y='counts',
    )

    enrollment_bar.update_layout(
        title=None,
        xaxis_title="Academic Year",
        yaxis_title=None,
        bargap=0.2,
        xaxis=dict(type='category'),
        margin=dict(t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return dcc.Graph(
        figure=enrollment_bar,
        config={"responsive": True},
        style={"width": "100%"}
    )





@callback(
    Output('highest-avg-enroll', 'children'),
    Output('year-text', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    
    # Extract required columns
    FILTERED_DF = FILTERED_DATA[['region', 'year', 'counts']]

    # Aggregate by year
    yearly_counts = FILTERED_DF.groupby('year')['counts'].sum()

    # Get highest year and value
    highest_year = yearly_counts.idxmax()
    highest_value = yearly_counts.max()

    # Optional: truncate number if needed
    truncated_highest_value = smart_truncate_number(highest_value)

    # Optional: print or return
    return f"{truncated_highest_value} Students", f"Academic Year {highest_year} - {highest_year+1}"




@callback(
    Output('high-avg-enroll', 'children'),
    Output('low-avg-enroll', 'children'),
    Output('high-tag-loc', 'children'),
    Output('low-tag-loc', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    
    # Extract required columns
    FILTERED_DF = FILTERED_DATA[['region', 'year', 'counts']]

    # Group by region and year, then compute total enrollments per year per region
    region_yearly_counts = FILTERED_DF.groupby(['region', 'year'])['counts'].sum().reset_index()

    # Now compute the average enrollment over the years for each region
    region_avg_enrollment = region_yearly_counts.groupby('region')['counts'].mean()

    # Find region with highest and lowest average enrollment
    highest_avg_region = region_avg_enrollment.idxmax()
    highest_avg_value = region_avg_enrollment.max()

    lowest_avg_region = region_avg_enrollment.idxmin()
    lowest_avg_value = region_avg_enrollment.min()

    # Truncate values if needed
    truncated_highest_avg = smart_truncate_number(highest_avg_value)
    truncated_lowest_avg = smart_truncate_number(lowest_avg_value)

    # Output (or return these values)
    return f"{truncated_highest_avg}", f"{truncated_lowest_avg}", f"{highest_avg_region}", f"{lowest_avg_region}"




@callback(
    Output('cloroplet', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DF = smart_filter(data, enrollment_db_engine)
    
    # Extract required columns
    # FILTERED_DF = FILTERED_DATA[['region', 'year', 'counts']]

    
    # FILTERED_DF = auto_extract(['province', 'counts'], is_specific=False)
    FILTERED_DF = FILTERED_DF.groupby('province', as_index=False)['counts'].sum()
        
        # Print for debug
    unique_provinces = FILTERED_DF['province'].drop_duplicates().tolist()
    print("Provinces in DataFrame:", len(unique_provinces))
    for province in sorted(unique_provinces):
        print(province)

    # Folder where all region-wise GeoJSON files are stored
    geojson_folder = project_root / "src/assets/_geojson/province"
    
    geojson_files = [
        "provinces-region-ph010000000.0.001.json",
        "provinces-region-ph020000000.0.001.json",
        "provinces-region-ph030000000.0.001.json",
        "provinces-region-ph040000000.0.001.json",
        "provinces-region-ph050000000.0.001.json",
        "provinces-region-ph060000000.0.001.json",
        "provinces-region-ph070000000.0.001.json",
        "provinces-region-ph080000000.0.001.json",
        "provinces-region-ph090000000.0.001.json",
        "provinces-region-ph100000000.0.001.json",
        "provinces-region-ph110000000.0.001.json",
        "provinces-region-ph120000000.0.001.json",
        "provinces-region-ph130000000.0.001.json",
        "provinces-region-ph140000000.0.001.json",
        "provinces-region-ph150000000.0.001.json",
        "provinces-region-ph160000000.0.001.json",
        "provinces-region-ph170000000.0.001.json",
        "provinces-region-ph180000000.0.001.json",

    ]

    # Combine all province GeoJSONs into one FeatureCollection
    all_features = []
    for filename in geojson_files:
        filepath = os.path.join(geojson_folder, filename)
        with open(filepath) as f:
            geo = json.load(f)
            geo = rewind(geo, rfc7946=False)
            all_features.extend(geo['features'])

    combined_geojson = {
        "type": "FeatureCollection",
        "features": all_features
    }

    # Extract province names from GeoJSON
    geo_provinces = [feature['properties']['ADM2_EN'] for feature in combined_geojson['features']]
    print("Provinces in GeoJSON:", len(set(geo_provinces)))
    print("Provinces in DataFrame:", len(set(FILTERED_DF['province'])))

    # Normalize for comparison
    df_norm = {name.strip().title() for name in unique_provinces}
    geo_norm = {name.strip().title() for name in geo_provinces}

    # Find unmatched from DataFrame
    unmatched = sorted(df_norm - geo_norm)

    print("\n❌ Unmatched provinces from DataFrame not found in GeoJSON:")
    for prov in unmatched:
        print(f"- {prov}")

    
    def normalize_province(name):
        if not name:
            return ""
        name = name.strip()

        # Common fixes
        name = name.replace("Ncr", "NCR")
        name = re.sub(r"(?i)^city of\s+", "", name)
        # name = re.sub(r",\s*NCR.*", "NCR", name)  # e.g., "Manila, NCR, First District" → "Manila NCR"
        name = unicodedata.normalize('NFKD', name)
        name = ''.join(c for c in name if not unicodedata.combining(c))
        return name.title()

    # Normalize both lists
    df_normalized = [normalize_province(name) for name in unique_provinces]
    geo_normalized = [normalize_province(name) for name in geo_provinces]

    # Convert to sets
    df_set = set(df_normalized)
    geo_set = set(geo_normalized)

    # Exact matches
    matched = sorted(df_set & geo_set)
    unmatched = sorted(df_set - geo_set)

    print("\n✅ Matched provinces:")
    for prov in matched:
        print(f"  ✅ {prov}")

    # Fuzzy match for unmatched
    fuzzy_matches = []
    for name in unmatched:
        best_match, score, _ = process.extractOne(name, geo_set, scorer=fuzz.ratio)
        if score >= 50:
            fuzzy_matches.append((name, best_match, score))

    # Output fuzzy matches
    print("\n🔁 Fuzzy matched provinces:")
    for original, matched, score in fuzzy_matches:
        print(f"  🔁 {original} ↔ {matched} ({score}%)")

    # Remaining unmatched after fuzzy match
    fuzzy_matched_names = {original for original, _, _ in fuzzy_matches}
    still_unmatched = sorted(set(unmatched) - fuzzy_matched_names)

    print("\n❌ Still unmatched provinces:")
    for prov in still_unmatched:
        print(f"  ❌ {prov}")
        
        
        # Step: Create mapping from fuzzy matches
    fuzzy_match_dict_prov = {original: matched for original, matched, _ in fuzzy_matches}

    # Step: Normalize and apply fuzzy match to province column in DF
    FILTERED_DF['normalized_province'] = FILTERED_DF['province'].apply(normalize_province)

    FILTERED_DF['final_province'] = FILTERED_DF['normalized_province'].apply(
        lambda x: fuzzy_match_dict_prov.get(x, x)  # Use fuzzy match if exists, else use normalized
    )

    # Step: Normalize GeoJSON province names (no uppercasing)
    geo_provinces_normalized_final = [normalize_province(p) for p in geo_provinces if p]

    # Step: Filter DataFrame to matching provinces
    FILTERED_DF = FILTERED_DF[
        FILTERED_DF['final_province'].isin(geo_provinces_normalized_final)
    ]

    # Step: Print unmatched final provinces (optional debug)
    unmatched_final = set(FILTERED_DF['final_province']) - set(geo_provinces_normalized_final)
    if unmatched_final:
        print("\n⚠️ Unmatched final provinces still not in GeoJSON:")
        for p in sorted(unmatched_final):
            print("  ❌", p)


    # 4. Plotly Choropleth
    map_chart = px.choropleth(
        FILTERED_DF,
        geojson=combined_geojson,
        locations='final_province',
        featureidkey='properties.ADM2_EN',
        color='counts',
        hover_name=None,
        hover_data=None,
        color_continuous_scale='Viridis',
        
    )
    
    map_chart.update_traces(
        hovertemplate="<b>%{location}</b><br>Total Enrollment: %{z:,}<extra></extra>"
    )


    map_chart.update_geos(
        visible=False,
        # showcountries=False,
        # showcoastlines=False,
        showland=True,
        fitbounds="locations",        # Ensures focus on actual geojson features
        center = {'lat':12.8797, 'lon':121.7740},
        resolution=50,
        lataxis_range=[4, 21],        # Latitude range for PH
        lonaxis_range=[115, 128],  # Longitude range for PH
    )



    map_chart.update_layout(
        # title="Enrollment by Region",
        # title_font=dict(size=20, family='Inter', color='#3C6382'),
        # title_x=0.5,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        height=900,
        width=700,
        # dragmode=False,
    )
    
    # map_chart.show(renderer="browser")
    return dcc.Graph(
        figure=map_chart,
        config={"responsive": True},
        # style={"width": "100%"}
    )