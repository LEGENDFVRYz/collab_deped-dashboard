import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State, Patch
from plotly.subplots import make_subplots 

# important part
from src.data import enrollment_db_engine, smart_filter

# Extra Utilities
from src.utils.extras_utils import smart_truncate_number


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
        'M': '#037DEE',
        'F': '#E11C38'
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
        title={
            'text': "Enrollment Distribution by Region and Gender",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': '#04508c'}
        },
        xaxis_title="Number of Students",
        yaxis_title="Region",
        legend_title="Gender",
        font=dict(color="#667889"),
        margin=dict(l=80, r=20, t=50, b=40),
        plot_bgcolor="#F5FBFF",
        paper_bgcolor="#F5FBFF",
    )

    return dcc.Graph(figure=gender_region_fig)

#################################################################################




# #################################################################################
# ##  --- CHART: enrollment density (students per location)
# #################################################################################
# # enrollment_density_chart = []





# #################################################################################



# #################################################################################
# ##  --- CHART: school sectors
# #################################################################################
# # enrollment_density_chart = []





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
            height=30  # header height
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
            height=60  # fixed cell height
        )
    )])

    hi_low_fig.update_layout(
        font=dict(family='Inter'),
        autosize=True,
        margin={"l": 8, "r": 8, "t": 15, "b": 0},
    )

    hi_low_fig
    
    return dcc.Graph(figure=hi_low_fig)

# #################################################################################