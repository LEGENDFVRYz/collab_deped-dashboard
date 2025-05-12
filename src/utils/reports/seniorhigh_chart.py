import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State

# important part
from src.data import enrollment_db_engine, smart_filter


# """
#     Analytics/SHS Tracks and Strands Charts and Indicator
    
# """


# #################################################################################
# ##                     MAIN DATAFRAME BASED FROM THE QUERY                     ##
# #################################################################################

# # ## -- This only a temporary dataframe for testing your charts, you can change it
# # FILTERED_DF = dataframe = auto_extract(['counts'], is_specific=False)
# # FILTERED_DF

# FILTERED_DF = dataframe = auto_extract(['shs_grade', 'sector'], is_specific=False)
# FILTERED_DF
# # ## -- Check the document for all valid columns and structurette
# # ## -- Dont change the all caps variables
# #################################################################################




# #################################################################################
# #################################################################################
# ## -- EXAMPLE CHHART

# # Manipulated Data for charts
# query = FILTERED_DF[['grade']][:]

# query['school-level'] = query['grade'].apply(
#     lambda x: 'JHS' if x in ['G7', 'G8', 'G9', 'G10', 'JHS'] else ('SHS' if x in ['G11', 'G12'] else 'ELEM')
# )

# query = query.groupby(['school-level', 'grade']).size().reset_index(name='school_count')

# # Ploting
# sample_chart = px.bar(
#     query,
#     x="school_count", 
#     y="grade",
#     color='school-level',
#     color_discrete_map={
#         'ELEM': '#FF899A', 
#         'JHS': '#E11C38', 
#         'SHS': '#930F22'
#     }
# )
# sample_chart

# sample_chart.update_layout(
#     autosize=True,
#     margin={"l": 8, "r": 8, "t": 8, "b": 8},  # Optional: Adjust margins
# )



# #################################################################################
# #################################################################################


# ## -- FIND YOUR CHARTS HERE:

# ################################################################################
# ##  --- Distribution of enrollees per track
# #################################################################################

@callback(
    Output('seniorhigh_distri_per_track', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    
    # Exclude "__NaN__" values in 'track'
    FILTERED_DATA['track'] = FILTERED_DATA['track'].astype(str).str.strip()
    FILTERED_DATA = FILTERED_DATA[(FILTERED_DATA['track'].str.upper() != '__NAN__') & (FILTERED_DATA['track'].notna())]
    
    # Group and prepare the data
    enrollees_distribution = FILTERED_DATA.groupby(['track'])['counts'].sum().reset_index()
    enrollees_distribution = enrollees_distribution.sort_values(by='counts', ascending=True)

    # Create the horizontal bar chart
    seniorhigh_distri_per_track = px.bar(
        enrollees_distribution,
        x='counts',
        y='track',
        orientation='h',
        labels={'counts': 'Number of Students', 'track': 'Track'}
    )

    # Update layout
    seniorhigh_distri_per_track.update_layout(
        bargap=0.2,  # Increase space between bars to make them appear thinner
        autosize=True,
        margin=dict(l=80, r=10, t=50, b=10),
        yaxis=dict(
            automargin=True,
            tickfont=dict(size=12),
        ),
        uirevision='true'
    )

    # Change the color and reduce the bar thickness
    seniorhigh_distri_per_track.update_traces(
        marker_color='#EF8292',
        width=0.2
    )

    return dcc.Graph(figure=seniorhigh_distri_per_track)


# #################################################################################




# #################################################################################
# ##  --- Ratio enrollment in Academic vs. non-Academic tracks
# #################################################################################

@callback(
    Output('seniorhigh_ratio_enrollment', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Count the number of students in each 'track'
    track_counts = FILTERED_DATA.groupby(['track'])['counts'].sum().reset_index(name='student_count')

    # Get the acad_count and non_acad_count
    acad_count = track_counts.loc[track_counts['track'] == 'ACADEMIC', 'student_count'].sum()
    non_acad_count = track_counts.loc[track_counts['track'].isin(['TVL', 'ARTS', 'SPORTS']), 'student_count'].sum()

    # Create the Donut Chart
    seniorhigh_ratio_enrollment = go.Figure(
        data=[go.Pie(
            labels=['Academic', 'Non-Academic'],
            values=[acad_count, non_acad_count],
            hole=0.7,  
            marker=dict(colors=['#5DB7FF', '#FF5B72']),
            textinfo='none',
            hoverinfo='label+value+percent',
            direction='clockwise',
            sort=False,
            domain={'x': [0, 1], 'y': [0, 1]},
        )]
    )

    # Update layout for true maximization
    seniorhigh_ratio_enrollment.update_layout(
        autosize=True,
        margin=dict(t=0, r=0, b=0, l=0),  
        showlegend=False,
        annotations=[
            dict(
                text="Academic<br>vs.<br>Non-Academic",
                x=0.5, y=0.5,
                font=dict(size=12, color='#3C6382'),  
                showarrow=False,
                align='center',
                xanchor='center',
                yanchor='middle'
            )
        ]
    )
    seniorhigh_ratio_enrollment
    
    return dcc.Graph(figure=seniorhigh_ratio_enrollment)

# #################################################################################



# #################################################################################
# ##  --- Most and least enrolled  (strand)
# #################################################################################

@callback(
    Output('seniorhigh_most_least_enrolled', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    # Filter out "__NaN__" and actual NaN values from 'strand'
    FILTERED_DATA['strand'] = FILTERED_DATA['strand'].astype(str).str.strip()
    FILTERED_DATA = FILTERED_DATA[(FILTERED_DATA['strand'].str.upper() != '__NAN__') & (FILTERED_DATA['strand'].notna())]

    # Group and sort by counts
    track_counts = FILTERED_DATA.groupby('strand')['counts'].sum().reset_index()
    sorted_tracks = track_counts.sort_values('counts', ascending=True)

    # Safely get most and least populated strands
    most_populated = sorted_tracks.sort_values('counts', ascending=False).iloc[0]
    least_populated = sorted_tracks.iloc[0]

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

    return dcc.Graph(figure=seniorhigh_most_least_enrolled)

# #################################################################################



# #################################################################################
# ##  --- Gender Distribution
# #################################################################################

@callback(
    Output('seniorhigh_gender_distri', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Remove "__NaN__" and actual NaN values from 'strand'
    FILTERED_DATA['strand'] = FILTERED_DATA['strand'].astype(str).str.strip()
    FILTERED_DATA = FILTERED_DATA[(FILTERED_DATA['strand'].str.upper() != '__NAN__') & (FILTERED_DATA['strand'].notna())]

    # Group the cleaned data by 'strand' and 'gender'
    track_gender = FILTERED_DATA.groupby(['strand', 'gender'])['counts'].sum().reset_index()

    # Calculate total counts per strand to determine sort order
    strand_order = (
        track_gender.groupby('strand')['counts']
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )

    # Create the horizontal bar chart with sorted strand order
    seniorhigh_gender_distri = px.bar(
        track_gender,
        x='counts',
        y='strand',
        category_orders={'strand': strand_order},  
        color='gender',
        orientation='h',
        barmode='group',
        labels={'strand': 'Strand', 'counts': 'Number of Students', 'gender': 'Gender'},
        color_discrete_sequence=['#5DB7FF', '#FF5B72']
    )
    
    seniorhigh_gender_distri.update_traces(width=0.2)


    # Update layout to maximize chart space and reduce label sizes
    seniorhigh_gender_distri.update_layout(
        autosize=True,
        margin=dict(l=60, r=10, t=50, b=20),        
        xaxis={
            'title': {'text': "Number of Students", 'font': {'color': '#667889', 'size': 11}},
            'tickfont': {'color': '#667889', 'size': 10},
        },
        yaxis={
            'title': {'text': "Strand", 'font': {'color': '#667889', 'size': 11}},
            'tickfont': {'color': '#667889', 'size': 10},
            'automargin': True
        },
        legend={
            'title': {'text': "Gender", 'font': {'color': '#667889', 'size': 10}},
            'font': {'color': '#667889', 'size': 10}
        },
        bargap=0.2,
        bargroupgap=0.025,
        uirevision='true',
    )
    seniorhigh_gender_distri

    return dcc.Graph(figure=seniorhigh_gender_distri)




#################################################################################



# #################################################################################
# ##  --- Differences in the number of schools offering each track
# #################################################################################

@callback(
    Output('seniorhigh_school_offering_per_track_by_sector', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Filter out "__NaN__" and actual NaN values from 'track'
    FILTERED_DATA['track'] = FILTERED_DATA['track'].astype(str).str.strip()
    FILTERED_DATA = FILTERED_DATA[(FILTERED_DATA['track'].str.upper() != '__NAN__') & (FILTERED_DATA['track'].notna())]
    
    # Group data by track and sector, counting unique schools
    filtered_data_df = FILTERED_DATA[FILTERED_DATA['counts'] != 0]
    school_count = filtered_data_df.groupby(['track', 'sector'])['beis_id'].nunique().reset_index(name='school_count')

    # Compute total school count per track to determine sort order
    track_order = (
        school_count.groupby('track')['school_count']
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )


    # Create horizontal stacked bar chart with sorted track order
    seniorhigh_school_offering_per_track_by_sector = px.bar(
        school_count,
        x='school_count',
        y='track',
        color='sector',
        orientation='h',
        labels={'school_count': 'Number of Schools', 'track': 'Track', 'sector': 'Sector'},
        color_discrete_sequence=['#02519B', '#0377E2', '#4FA4F3', '#9ACBF8'],
        category_orders={'track': track_order},
    
    )
    
    seniorhigh_school_offering_per_track_by_sector.update_traces(width=0.2)


    # Update layout
    seniorhigh_school_offering_per_track_by_sector.update_layout(        
        xaxis={
            'title': {'text': "Number of Schools", 'font': {'color': '#667889'}},
            'tickfont': {'color': '#667889'},
            'tickformat': '~s',
            'tickangle': 0
        },
        yaxis={
            'title': {'text': "Track", 'font': {'color': '#667889'}},
            'tickfont': {'color': '#667889'}
        },
        legend={
            'title': {'text': "Sector", 'font': {'color': '#667889'}},
            'font': {'color': '#667889'}
        },
        bargap=0.2,
        autosize=True,
        margin=dict(l=80, r=40, t=60, b=40)
    )
    seniorhigh_school_offering_per_track_by_sector

    return dcc.Graph(figure=seniorhigh_school_offering_per_track_by_sector)
    
#################################################################################



# #################################################################################
# ##  --- Which SHS tracks are least offered but in high demand
# #################################################################################

@callback(
    Output('seniorhigh_least_offered_high_demand', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Filter out "__NaN__" and actual NaN values from 'track'
    FILTERED_DATA['track'] = FILTERED_DATA['track'].astype(str).str.strip()
    FILTERED_DATA = FILTERED_DATA[(FILTERED_DATA['track'].str.upper() != '__NAN__') & (FILTERED_DATA['track'].notna())]
    
    # Group by track to get supply and demand
    grouped = FILTERED_DATA.groupby('track').agg(
        offerings=('beis_id', 'count'),    
        total_demand=('counts', 'sum')    
    ).reset_index()

    # Define custom color palette
    custom_colors = ['#00CCFF', '#1389F0', '#0C6DC1', '#074889']

    # Create the scatter plot
    seniorhigh_least_offered_high_demand = px.scatter(
        grouped,
        x='offerings',
        y='total_demand',
        color='track',
        labels={
            'offerings': 'Number of Offerings (Supply)',
            'total_demand': 'Student Demand',
            'track': 'SHS Track',
        },
        color_discrete_sequence=custom_colors
    )

    # Update layout for full responsiveness and clean space usage
    seniorhigh_least_offered_high_demand.update_layout(
        autosize=True,
        margin=dict(l=60, r=100, t=80, b=60),        
        xaxis=dict(
            title=dict(text='Number of Offerings (Supply)', font=dict(color='#667889', size=12)),
            tickfont=dict(color='#667889'),
            automargin=True
        ),
        yaxis=dict(
            title=dict(text='Student Demand', font=dict(color='#667889', size=12)),
            tickfont=dict(color='#667889'),
            automargin=True
        ),
        legend=dict(
            title=dict(text='SHS Track', font=dict(color='#667889')),
            font=dict(color='#667889'),
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.02  
        )
    )

    # Display the chart
    seniorhigh_least_offered_high_demand

    return dcc.Graph(figure=seniorhigh_least_offered_high_demand)
    
#################################################################################



# #################################################################################
# ##  --- How many schools offer each SHS track per region
# #################################################################################

@callback(
    Output('seniorhigh_shs_offers', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    schooloffer_region = FILTERED_DATA[
        FILTERED_DATA['strand'].notna() & 
        (FILTERED_DATA['strand'] != '__NaN__')
    ]

    # Step 1: Filter only rows where counts > 0
    valid_offers = schooloffer_region[schooloffer_region['counts'] > 0]

    # Step 2: Drop duplicates so that each school only counts once per strand-region
    valid_offers_unique = valid_offers.drop_duplicates(subset=['beis_id', 'region', 'strand'])

    # Step 3: Group by region and strand, count number of unique schools offering each
    heatmap_data = valid_offers_unique.groupby(['region', 'strand']).size().reset_index(name='school_count')

    # Step 4: Pivot for heatmap structure
    heatmap_pivot = heatmap_data.pivot(index='strand', columns='region', values='school_count').fillna(0)

    # Step 5: Color scale with white for 0
    colorscale = [
        [0.0, "#ffffff"],    # white for 0
        [0.00001, "#FF899A"],  # light pink
        [0.5, "#E11C38"],    # mid red
        [1.0, "#930F22"]     # deep red
    ]

    # Step 6: Create the heatmap
    heatmap_fig = px.imshow(
        heatmap_pivot.values,
        labels=dict(x="Region", y="SHS Strand", color="Number of Schools Offering"),
        x=heatmap_pivot.columns.tolist(),
        y=heatmap_pivot.index.tolist(),
        color_continuous_scale=colorscale,
        zmin=0,
        zmax=heatmap_pivot.values.max()
    )

    # Step 7: Layout tweaks
    heatmap_fig.update_layout(
        title="Number of Schools Offering SHS Strands per Region",
        xaxis_title="Region",
        yaxis_title="SHS Strand",
        xaxis=dict(tickangle=45),
        margin={"l": 40, "r": 40, "t": 50, "b": 40}
    )

    heatmap_fig
    
    return dcc.Graph(figure=heatmap_fig)

# #################################################################################



# #################################################################################
# ##  --- Which SHS tracks are more prevalent in each sector
# #################################################################################

@callback(
    Output('seniorhigh_prevalent_tracks', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # Filter out rows with NaN or "__NaN__" in 'strand'
    FILTERED_byprevalent = FILTERED_DATA[
        FILTERED_DATA['strand'].notna() &
        (FILTERED_DATA['strand'] != '__NaN__')
    ]

    # Calculate total counts per grade (if needed elsewhere)
    grade_enrollment2 = FILTERED_DATA.groupby('grade')['counts'].sum().reset_index()

    # Merge counts with strand + sector
    merged = FILTERED_byprevalent.copy()
    merged['counts'] = FILTERED_DATA['counts']

    # Group by strand and sector
    grouped = merged.groupby(['strand', 'sector'])['counts'].sum().reset_index()

    # Smart number formatting
    def smart_truncate_number(num):
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return str(num)

    grouped['counts_text'] = grouped['counts'].apply(smart_truncate_number)

    # Define blue color shades
    blue_shades = ['#012C53', '#023F77', '#02519B', '#0264BE', '#0377E2']

    # Create grouped bar chart
    prevalent_tracks_fig = px.bar(
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

    # Set text and layout options
    prevalent_tracks_fig.update_traces(textposition='outside')

    prevalent_tracks_fig.update_layout(
        xaxis_tickangle=-45,
        legend_title='Sector',
        xaxis_title='SHS Strand',
        yaxis_title='Number of Students',
        margin=dict(l=60, r=40, t=60, b=60)
    )

    prevalent_tracks_fig

    return dcc.Graph(figure=prevalent_tracks_fig)

# #################################################################################



# #################################################################################
# ##  --- Do mother schools or annexes offer a wider range of SHS tracks
# #################################################################################

@callback(
    Output('shs_offer_range', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    track_counts = FILTERED_DATA.groupby('type')['strand'].nunique().reset_index()
    track_counts.columns = ['School Type', 'Number of strand']

    blue_shades = ['#012C53', '#023F77', '#02519B', '#0264BE', '#0377E2']

    track_counts = FILTERED_DATA.groupby('type')['strand'].nunique().reset_index()
    track_counts.columns = ['School Type', 'Number of strand']

    shs_offer_range = px.bar(
        track_counts,
        x='School Type',
        y='Number of strand',
        title='Number of SHS Strand Offered by Mother Schools vs Annexes',
        color='School Type',
        text='Number of strand',
        color_discrete_sequence=blue_shades
    )

    shs_offer_range.update_traces(textposition='outside')

    shs_offer_range.update_layout(
        xaxis_title='School Type',
        yaxis_title='Number of Strand Offered',
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        showlegend=False
    )

    shs_offer_range
    
    return dcc.Graph(figure=shs_offer_range)

