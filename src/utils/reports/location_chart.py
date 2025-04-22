import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State, Patch

# important part
from src.data import enrollment_db_engine, smart_filter

# Extra Utilities
from plotly.subplots import make_subplots 
from utils.reports.home_enrollment_per_region import smart_truncate_number


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




## -- FIND YOUR CHARTS HERE:

################################################################################
##  --- CHART: Distribution of enrollees per location 
#################################################################################

@callback(
    Output('location_enrollees-distribution-per-location', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # Step 1: Group by region and gender
    gender_region = FILTERED_DATA.groupby(['region', 'gender'])['counts'].sum().reset_index()

# Step 2: Define brand colors
    brand_colors = {
        'M': '#5DB7FF',
        'F': '#FF5B72'
    }

    # Step 3: Create the stacked bar chart
    gender_region_fig = px.bar(
        gender_region,
        x='counts',
        y='region',
        color='gender',
        orientation='h',
        barmode='stack',
        labels={'counts': 'Number of Enrollees', 'region': 'Region', 'gender': 'Gender'},
        color_discrete_map=brand_colors
    )

    # Step 4: Calculate total per region for annotations
    region_totals = gender_region.groupby('region')['counts'].sum().reset_index()

    # Step 5: Add truncated total annotations using your function
    for _, row in region_totals.iterrows():
        short_text = smart_truncate_number(row['counts'])  # Your custom truncation
        gender_region_fig.add_annotation(
            x=row['counts'] + 1,
            y=row['region'],
            text=short_text,
            hovertext=str(row['counts']),  # Full raw number on hover
            showarrow=False,
            font=dict(color="#04508c", size=12),
            xanchor="left",
            yanchor="middle"
        )

    # Step 6: Customize layout
    gender_region_fig.update_layout(
        xaxis_title="Number of Students",
        yaxis_title="Region",
        legend_title="Gender",
        font=dict(color="#667889", family='Inter'),
        margin=dict(l=80, r=20, t=20, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    gender_region_fig

    return dcc.Graph(figure=gender_region_fig)

#################################################################################




# #################################################################################
# ##  --- CHART: enrollment density (students per location)
# #################################################################################
# # enrollment_density_chart = []

# import pandas as pd
# import plotly.express as px
# import json
# from geojson_rewind import rewind
# # Load your enrollment data
# # FILTERED_DF is already provided
# # FILTERED_DF = pd.read_csv("your_filtered_df.csv")  # if from CSV

# # ## -- This only a temporary dataframe for testing your charts, you can change it
# FILTERED_DF = dataframe = auto_extract(['counts', 'region', 'brgy'], is_specific=False)
# FILTERED_DF[['region', 'province', 'division', 'district', 'municipality', 'brgy', 'counts']]


# # Load GeoJSON (municipality level for PH)
# with open("/Users/marke/Downloads/country.0.1.json") as f:
#     geojson = json.load(f)

# geojson = rewind(geojson, rfc7946=False)

# # Print all REGION names in GeoJSON
# geo_regions = [feature['properties']['adm1_en'] for feature in geojson['features']]
# print(set(geo_regions))

# # Print all region names in your DF
# print(set(FILTERED_DF['region']))


# region_name_map = {
#     'Region I': 'Region I (Ilocos Region)',
#     'Region II': 'Region II (Cagayan Valley)',
#     'Region III': 'Region III (Central Luzon)',
#     'Region IV-A': 'Region IV-A (CALABARZON)',
#     'Region IV-B': 'Region IV-B (MIMAROPA)',
#     'Region V': 'Region V (Bicol Region)',
#     'Region VI': 'Region VI (Western Visayas)',
#     'Region VII': 'Region VII (Central Visayas)',
#     'Region VIII': 'Region VIII (Eastern Visayas)',
#     'Region IX': 'Region IX (Zamboanga Peninsula)',
#     'Region X': 'Region X (Northern Mindanao)',
#     'Region XI': 'Region XI (Davao Region)',
#     'Region XII': 'Region XII (SOCCSKSARGEN)',
#     'Region XIII': 'Region XIII (Caraga)',
#     'NCR': 'National Capital Region (NCR)',
#     'CAR': 'Cordillera Administrative Region (CAR)',
#     'BARMM': 'Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)',  # or ARMM depending on version
#     # Add others if needed
# }
# # Map region names to GeoJSON-compatible names
# FILTERED_DF['geo_region'] = FILTERED_DF['region'].map(region_name_map)
# FILTERED_DF = FILTERED_DF.dropna(subset=['geo_region'])  # remove rows without mapping

# # Plot the map
# fig = px.choropleth(
#     FILTERED_DF,
#     geojson=geojson,
#     locations='geo_region',
#     featureidkey='properties.adm1_en',
#     color='counts',
#     hover_name='region',
#     hover_data=['province', 'counts'],
#     color_continuous_scale='Viridis',
# )

# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(title="Enrollment by Region", margin={"r":0,"t":30,"l":0,"b":0})
# fig




#################################################################################



# #################################################################################
# ##  --- CHART: school sectors
# #################################################################################

@callback(
    Output('location_school_sectors', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # 2. Aggregate counts by region and sector, then sort so smaller sectors stack on top
    sector_enrollment = (
        FILTERED_DATA
        .groupby(['region', 'sector'])['counts']
        .sum()
        .reset_index()
    )

    # Sort within each region by counts ascending (smallest on top in stack)
    sector_enrollment = (
        sector_enrollment
        .sort_values(['region', 'counts'], ascending=[True, True])
    )

    # 3. Define chronological region order (DepEd standard)
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

    # 4. Define exact sector order and use red shades from your palette
    sector_order  = ['Public', 'Private', 'SUCs/LUCs', 'PSO']
    sector_colors = {
        'Public':    '#930F22',  # Dark red
        'Private':   '#E11C38',  # Mid red
        'SUCs/LUCs': '#FF5B72',  # Light red
        'PSO':       '#FF899A'   # Pinkish red
    }

    # Enforce sector order to control stacking
    sector_enrollment['sector'] = pd.Categorical(
        sector_enrollment['sector'],
        categories=sector_order,
        ordered=True
    )

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

    # 6. Uniform styling with y-axis tickformat as "4M", "5M", etc.
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
            tickprefix=''
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
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # Step 2: Group and SUM the 'counts' for track-level heatmap
    track_data = FILTERED_DATA.groupby(['region', 'track'])['counts'].sum().reset_index()
    track_pivot = track_data.pivot(index='track', columns='region', values='counts').fillna(0)

    # Step 3: Group and SUM the 'counts' for strand-level heatmap
    strand_data = FILTERED_DATA.groupby(['region', 'strand'])['counts'].sum().reset_index()
    strand_pivot = strand_data.pivot(index='strand', columns='region', values='counts').fillna(0)

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
        title_text="Student Enrollment",
        xaxis2=dict(title="Region", tickangle=45),
        yaxis=dict(title="Track"),
        yaxis2=dict(title="Strand"),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Step 6: Show the figure
    heatmap_fig

    return dcc.Graph(figure=heatmap_fig)

# #################################################################################



# #################################################################################
# ##  --- INDICATOR: Total number of enrollees
# #################################################################################

@callback(
    Output('raw-total-enrollees', 'children'),
    Output('truncated-total-enrollees', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    raw_total_enrollees = FILTERED_DATA['counts'].sum()
    truncated_total_enrollees = smart_truncate_number(raw_total_enrollees)

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
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    # Count total number of unique schools
    raw_total_schools = FILTERED_DATA['name'].nunique()
    truncated_total_schools = smart_truncate_number(raw_total_schools)

    raw_total_schools
    truncated_total_schools
    
    return f"{raw_total_schools:,} enrollees", truncated_total_schools

# #################################################################################



# #################################################################################
# ##  --- TABLE: Total number of schools
# #################################################################################

@callback(
    Output('location_highest_lowest_enrollees', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # Step 1: Group by school and region, summing the counts
    aggregated_df = FILTERED_DATA.groupby(['name', 'region'], as_index=False)['counts'].sum()

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
            fill_color='#EA6074',
            align='left',
            font=dict(family='Inter', color='#9DADBD', size=13),
            line_color='white',
            height=40  # header height
        ),
        cells=dict(
            values=[
                highest_lowest2['name'].apply(lambda x: f"{x}\n"),
                highest_lowest2['region'],
                highest_lowest2['counts']
            ],
            fill_color='#F8C6CD',
            align='left',
            font=dict(family='Inter', color='#667889', size=13),
            height=100  # fixed cell height
        )
    )])

    hi_low_fig.update_layout(
        font=dict(family='Inter', color='#667889', size=13),
        autosize=True,
        margin={"l": 8, "r": 8, "t": 15, "b": 0},
    )

    hi_low_fig
    
    return dcc.Graph(figure=hi_low_fig)

# #################################################################################