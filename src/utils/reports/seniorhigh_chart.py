import time
from turtle import title
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State 

# important part
from src.data import enrollment_db_engine, smart_filter
from src.utils.extras_utils import smart_truncate_number


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
    State('is-all-year', 'data')
    # prevent_initial_call=True
)

def update_graph(trigger, data, mode):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    cleaned_df = FILTERED_DATA[FILTERED_DATA['track'] != '__NaN__']
    cleaned_df['track'] = cleaned_df['track'].cat.remove_unused_categories()
    
    grouped_by_tracks = cleaned_df.groupby(["track"], as_index=False)["counts"].sum()
    
    # Extract and group data
    if mode:
        grouped_by_tracks = grouped_by_tracks.sort_values(by="counts", ascending=False)
        grouped_by_tracks['counts_truncated'] = grouped_by_tracks['counts'].apply(smart_truncate_number)
        
    else:
        grouped_by_tracks = grouped_by_tracks.groupby('track', as_index=False)['counts'].mean()
        grouped_by_tracks = grouped_by_tracks.sort_values(by="counts", ascending=False)
        grouped_by_tracks['counts_truncated'] = grouped_by_tracks['counts'].apply(smart_truncate_number)

    # Create bar chart
    seniorhigh_distri_per_track = px.bar(
        grouped_by_tracks,
        x="track",
        y="counts",
        color="track",
        text="counts_truncated",
        color_discrete_sequence=["#B4162D", "#D61B35", "#E63E56", "#EA6074"]
    )

    # Update layout
    seniorhigh_distri_per_track.update_layout(
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=False,
        xaxis=dict(
            tickfont=dict(size=10, color="#667889", family="Inter, sans-serif"),
            title=None,
            showgrid=False,
        ),
        yaxis=dict(
            type='log',
            tickvals=[10000, 100000, 1000000, 2000000],
            ticktext=["10K", "100K", "1M", "2M"],
            tickfont=dict(size=10, color="#667889", family="Inter, sans-serif"),
            title=None,
            showgrid=True,
            gridcolor='#D2EBFF',
            ticksuffix="  ",
        ),
    )

    # Update traces
    seniorhigh_distri_per_track.update_traces(
        textposition='outside',
        insidetextanchor='middle',
        textfont=dict(size=10, color="#667889", family="Inter, sans-serif"),
        hovertemplate='Track: %{x}<br>Count: %{y}<extra></extra>',
    )
    
    return dcc.Graph(figure=seniorhigh_distri_per_track, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #################################################################################




# #################################################################################
# ##  --- Ratio enrollment in Academic vs. non-Academic tracks
# #################################################################################
@callback(
    Output('seniorhigh_ratio_enrollment', 'children'),
    Output('acad-count', 'children'),
    Output('non-acad-count', 'children'),
    Output('acad-percentage', 'children'),
    Output('non-acad-percentage', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    State('is-all-year', 'data')
    # prevent_initial_call=True
)

def update_graph(trigger, data, mode):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    cleaned_df = FILTERED_DATA[FILTERED_DATA['track'] != '__NaN__']
    cleaned_df['track'] = cleaned_df['track'].cat.remove_unused_categories()
    
    if mode:
        # Count the number of students in each 'track'
        track_counts = cleaned_df.groupby(['track'])['counts'].sum().reset_index(name='student_count')
        
    else:
        track_counts = cleaned_df.groupby(['year', 'track'])['counts'].sum().reset_index()
        track_counts = track_counts.groupby('track', as_index=False)['counts'].mean()
        track_counts['counts'] = track_counts['counts'].round(0).astype(int)
        track_counts.rename(columns={'counts': 'student_count'}, inplace=True)
        
    acad_count = track_counts.loc[track_counts['track'] == 'ACADEMIC', 'student_count'].sum()
    non_acad_count = track_counts.loc[track_counts['track'].isin(['TVL', 'ARTS', 'SPORTS']), 'student_count'].sum()
    total = acad_count + non_acad_count

    # Labels and values for visual half-donut effect
    labels = ['Academic', 'Non-Academic', 'Total']
    values = [acad_count, non_acad_count, total]
    colors = ['#037DEE', '#E11C38', '#FFFFFF'] 

    # Manually calculate true percentages
    true_percentages = [
        f"{(acad_count / (total)) * 100:.1f}%",
        f"{(non_acad_count / (total)) * 100:.1f}%",
        ""
    ]
    
    acad_percentage = f"{(acad_count / (total)) * 100:.1f}%",
    non_acad_percentage = f"{(non_acad_count / (total)) * 100:.1f}%",

    # Create Figure
    seniorhigh_ratio_enrollment = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.72,
            marker=dict(colors=colors),
            textinfo='none',
            hoverinfo='skip',  # disable default
            customdata=true_percentages,
            hovertemplate="%{label}<br>%{value} students<br>%{customdata}<extra></extra>",
            direction='clockwise',
            sort=False,
            rotation=270,
            domain={'x': [0, 1], 'y': [0.1, 1]}
        )]
    )

    seniorhigh_ratio_enrollment.update_layout(
        autosize=True,
        margin=dict(t=0, r=0, b=16, l=5),
        showlegend=False,
        annotations=[
            dict(
                text="<b>Academic vs.<br>Non-Academic<b>",
                x=0.5, y=0.64,
                font=dict(size=16, color="#3C6382", family="Inter Bold, Inter, sans-serif"),
                showarrow=False,
                align='center',
                xanchor='center',
                yanchor='middle'
            )
        ]
    )
        
    return (dcc.Graph(figure=seniorhigh_ratio_enrollment, config={"responsive": True}, style={"width": "100%", "height": "200%"},),
            f"{acad_count:,}", f"{non_acad_count:,}", acad_percentage, non_acad_percentage)

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
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    cleaned_df = FILTERED_DATA[FILTERED_DATA['strand'] != '__NaN__']
    cleaned_df['strand'] = cleaned_df['strand'].cat.remove_unused_categories()

    # Group and find the most and least populated strands
    track_counts = cleaned_df.groupby('strand')['counts'].sum().reset_index()
    most_populated = track_counts.sort_values('counts', ascending=False).iloc[0]
    least_populated = track_counts.sort_values('counts', ascending=True).iloc[0]

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
    
    seniorhigh_most_least_enrolled
    
    return dcc.Graph(figure=seniorhigh_most_least_enrolled, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #################################################################################



# #################################################################################
# ##  --- Gender Distribution
# #################################################################################
@callback(
    Output('seniorhigh_gender_distri', 'children'),
    Output('shs-highest-strand', 'children'),
    Output('shs-highest-count', 'children'),
    Output('shs-lowest-strand', 'children'),
    Output('shs-lowest-count', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Remove "__NaN__" and actual NaN values from 'strand'
    cleaned_df = FILTERED_DATA[FILTERED_DATA['strand'] != '__NaN__']
    cleaned_df['strand'] = cleaned_df['strand'].cat.remove_unused_categories()

    # Group the cleaned data by 'strand' and 'gender'
    track_gender = cleaned_df.groupby(['strand', 'gender'])['counts'].sum().reset_index()

    # Calculate total counts per strand to determine sort order
    strand_order = (
        track_gender.groupby('strand')['counts']
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )
    
    strand_totals = track_gender.groupby('strand')['counts'].sum()
    
    highest_strand = strand_totals.idxmax()
    highest_count = strand_totals.max()
    lowest_strand = strand_totals.idxmin()
    lowest_count = strand_totals.min()

    # Create the horizontal bar chart with sorted strand totals
    seniorhigh_gender_distri = px.bar(
        track_gender,
        x='counts',
        y='strand',
        category_orders={'strand': strand_order},  
        color='gender',
        orientation='h',
        barmode='group',
        labels={'strand': 'Strand', 'counts': 'Number of Students', 'gender': 'Gender'},
        color_discrete_sequence=['#FF5B72', '#5DB7FF']
    )

    # Update layout to maximize chart space and reduce label sizes
    seniorhigh_gender_distri.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        title=None,
        xaxis= dict(
            title=None,
            tickfont=dict(size=10, color="#667889", family="Inter, sans-serif"),
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=10, color="#667889", family="Inter, sans-serif"),
        ),
        legend=dict(
            title='Gender',
            font=dict(size=10, color="#667889", family="Inter, sans-serif"),
            orientation='h',      # horizontal layout
            yanchor='bottom',
            y=1.02,               # slightly above the plot
            xanchor='center',
            x=0.5,                # centered horizontally
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
        ),
        # annotations=[
        #     dict(
        #         text="Gender",
        #         x=0.5,
        #         y=1.12,  # Position above legend
        #         xref="paper",
        #         yref="paper",
        #         showarrow=False,
        #         font=dict(size=10, color="#667889"),
        #         xanchor='center'
        #     )
        # ],
        
        bargap=0.3,
        bargroupgap=0.05,
        uirevision='true',
    )
    
    seniorhigh_gender_distri
    
    return (
        dcc.Graph(figure=seniorhigh_gender_distri, config={"responsive": True}, style={"width": "100%", "height": "100%"}),
        highest_strand,
        f"{highest_count:,}",
        lowest_strand,
        f"{lowest_count:,}"
    )

# #################################################################################



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
    
    # Group data by track and sector, counting unique schools
    cleaned_df = FILTERED_DATA[FILTERED_DATA['track'] != '__NaN__']
    cleaned_df['track'] = cleaned_df['track'].cat.remove_unused_categories()
    filtered_data_df = cleaned_df[cleaned_df['counts'] != 0]
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

    # Update layout
    seniorhigh_school_offering_per_track_by_sector.update_layout(
        autosize=True,
        title=None,
        xaxis=dict(
            title=None,
            tickfont=dict(size=10, color="#667889", family="Inter, sans-serif"),
            tickformat="~s",
            tickangle=0
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=10, color="#667889", family="Inter, sans-serif")
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.3,  # Adjust as needed to avoid clipping
            xanchor='center',
            x=0.5,
            title=dict(
                text="Sector",
                font=dict(size=10, color="#667889", family="Inter, sans-serif")
            ),
            font=dict(size=10, color="#667889", family="Inter, sans-serif")
        ),
        bargap=0.3,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    seniorhigh_school_offering_per_track_by_sector.update_traces(marker_line_width=0)
    seniorhigh_school_offering_per_track_by_sector
    
    return dcc.Graph(figure=seniorhigh_school_offering_per_track_by_sector, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #################################################################################



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
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
   
    # Clean the 'track' column
    FILTERED_DATA['track'] = FILTERED_DATA['track'].astype(str).str.strip()
    FILTERED_DATA = FILTERED_DATA[
        (FILTERED_DATA['track'].str.upper() != '__NAN__') & (FILTERED_DATA['track'].notna())
    ]


    # Group by track to get offerings (supply) and total student demand
    grouped = FILTERED_DATA.groupby('track').agg(
        offerings=('beis_id', 'count'),
        total_demand=('counts', 'sum')
    ).reset_index()

    # Create the bubble chart (scatter with size)
    seniorhigh_least_offered_high_demand = px.scatter(
        grouped,
        x='offerings',
        y='track',
        size='total_demand',
        size_max=50,
        labels={
            'offerings': 'Number of Offerings (Supply)',
            'total_demand': 'Student Demand',
            'track': 'SHS Track'
        }
    )


    # Set all markers to the same color manually
    seniorhigh_least_offered_high_demand.update_traces(marker=dict(color='#0264BE'))


    # Update layout to remove legend and apply custom styles
    seniorhigh_least_offered_high_demand.update_layout(
        autosize=True,
        height=None, 
        width=None,
        xaxis=dict(
            title=None,
            tickfont=dict(size=10, color="#667889", family="Inter, sans-serif"),
            automargin=True
        ),
        yaxis=dict( 
            title=None,           
            tickfont=dict(size=10, color="#667889", family="Inter, sans-serif"),
            categoryorder='total ascending',
            automargin=True
        ),
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )
   
    # Displays the chart.
    seniorhigh_least_offered_high_demand

    
    return dcc.Graph(figure=seniorhigh_least_offered_high_demand, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #################################################################################



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

    cleaned_df = FILTERED_DATA[FILTERED_DATA['strand'] != '__NaN__']
    cleaned_df['strand'] = cleaned_df['strand'].cat.remove_unused_categories()

    # Step 1: Filter only rows where counts > 0
    valid_offers = cleaned_df[cleaned_df['counts'] > 0]

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

    heatmap_fig.update_layout(
        title=None,
        margin=dict(l=0, r=0, t=0, b=0),  # Slightly smaller bottom margin
        autosize=True,
        xaxis=dict(
            title=None,
            tickangle=-45,
            tickfont=dict(size=10, color="#667889")
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=10, color="#667889"),
            ticksuffix="  "
        ),
        coloraxis_colorbar=dict(
            orientation='h',      # horizontal bar
            title="",             
            thickness=12,         
            len=1.0,
            x=0.5,                # center horizontally
            xanchor='center',
            y=-0.1,               # closer to heatmap
            yanchor='top'
        )
    )
    
    heatmap_fig.update_coloraxes(showscale=True)
    
    return dcc.Graph(figure=heatmap_fig, config={"responsive": True}, style={"width": "100%", "height": "100%"})



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
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    cleaned_df = FILTERED_DATA[FILTERED_DATA['strand'] != '__NaN__']
    cleaned_df['strand'] = cleaned_df['strand'].cat.remove_unused_categories()

    # Calculate total counts per grade (if needed elsewhere)
    grade_enrollment2 = cleaned_df.groupby('grade')['counts'].sum().reset_index()

    # Merge counts with strand + sector
    merged = cleaned_df.copy()
    merged['counts'] = cleaned_df['counts']

    # Group by strand and sector
    grouped = merged.groupby(['strand', 'sector'])['counts'].sum().reset_index()
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
        labels={'strand': 'SHS Strand', 'counts': 'Number of Students', 'sector': 'School Sector'},
        color_discrete_sequence=blue_shades,
        text='counts_text'
    )

    # Set text and layout options
    prevalent_tracks_fig.update_traces(
        textposition="outside",
        textfont=dict(size=8, color="#04508c"),
    )

    prevalent_tracks_fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            title="Sector",
            font=dict(size=12)
        ),
        title=None,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(title=None),
        yaxis=dict(
            type='log',
            tickvals=[100, 1000, 10000, 100000, 500000, 1000000],
            ticktext=["100", "1000", "10K", "100K", "500K", "1M"],
            title=None,
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        paper_bgcolor='rgba(0,0,0,0)'  # Transparent figure background
    )

    return dcc.Graph(figure=prevalent_tracks_fig, config={"responsive": True}, style={"width": "100%", "height": "100%"})


# #################################################################################



# #################################################################################
# ##  --- Do mother schools or annexes offer a wider range of SHS tracks
# #################################################################################

@callback(
    Output('seniorhigh_offer_range', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    cleaned_df = FILTERED_DATA[FILTERED_DATA['strand'] != '__NaN__']
    cleaned_df['strand'] = cleaned_df['strand'].cat.remove_unused_categories()

    blue_shades = ['#012C53', '#023F77', '#02519B', '#0264BE', '#0377E2']

    track_counts = cleaned_df.groupby('type')['strand'].nunique().reset_index()
    track_counts.columns = ['School Type', 'Number of strand']

    shs_offer_range = px.bar(
        track_counts,
        x='School Type',
        y='Number of strand',
        # title='Number of SHS Strand Offered by Mother Schools vs Annexes',
        color='School Type',
        text='Number of strand',
        color_discrete_sequence=blue_shades
    )

    shs_offer_range.update_traces(textposition='outside')

    shs_offer_range.update_layout(
        # xaxis_title='School Type',
        # yaxis_title='Number of Strand Offered',
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            title=None,
        ),
        yaxis=dict(
            title=None,
        )
    )

    shs_offer_range
    
    return dcc.Graph(figure=shs_offer_range, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #################################################################################
# ##  --- year-over-year enrollment trend for each SHS track
# #################################################################################

@callback(
    Output('seniorhigh_year_over_year', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    # Ensure 'year' is numeric and clean the data
    FILTERED_DATA['year'] = pd.to_numeric(FILTERED_DATA['year'], errors='coerce')
    FILTERED_DATA = FILTERED_DATA.dropna(subset=['year'])
    FILTERED_DATA['year'] = FILTERED_DATA['year'].astype(int)

    cleaned_df = FILTERED_DATA[FILTERED_DATA['track'] != '__NaN__']
    cleaned_df['track'] = cleaned_df['track'].cat.remove_unused_categories()

    # Group by year and track
    grouped_df = cleaned_df.groupby(['year', 'track'], as_index=False)['counts'].sum()

    # Custom colors
    custom_colors = ['#02519B', '#0377E2', '#4FA4F3', '#9ACBF8']

    # Create the line chart
    seniorhigh_year_over_year = px.line(
        grouped_df,
        x='year',
        y='counts',
        color='track',
        markers=True,
        line_shape='spline',
        color_discrete_sequence=custom_colors,
        labels={
            'year': 'Year',
            'counts': 'Number of Students',
            'track': 'Track'
        }
    )

    # Apply visual enhancements
    seniorhigh_year_over_year.update_traces(
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=8, symbol='circle', line=dict(width=1, color='white')),
        textposition='top center'
    )

    # Update layout for visual clarity
    seniorhigh_year_over_year.update_layout(
        template='plotly_white',
        autosize=True,
        font=dict(family='Inter, sans-serif', color='#667889', size=12),
        legend=dict(
            title=None,
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(size=13)
        ),
        margin=dict(l=12, r=12, t=12, b=12),
        xaxis=dict(
            type='category',
            tickfont=dict(size=11, color='#667889'),
            showline=True,
            linecolor="#3C6382",
            linewidth=1,
            title=None
        ),
        yaxis=dict(
            tickformat="~s",
            tickfont=dict(size=11, color='#667889'),
            showline=True,
            linecolor="#3C6382",
            linewidth=1,
            title=None,
            ticksuffix="  ",
        )
    )
    
    return dcc.Graph(figure=seniorhigh_year_over_year, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #################################################################################
# ##  --- enrollment comparison over the years (per strand)
# #################################################################################

@callback(
    Output('seniorhigh_enrollment_comparison_per_strand', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # Filter out null values.
    FILTERED_DATA['year'] = pd.to_numeric(FILTERED_DATA['year'], errors='coerce')
    FILTERED_DATA['strand'] = FILTERED_DATA['strand'].astype(str).str.strip()
    FILTERED_DATA = FILTERED_DATA[(FILTERED_DATA['strand'].str.upper() != '__NAN__') & (FILTERED_DATA['strand'].notna())]  
    FILTERED_DATA['year'] = FILTERED_DATA['year'].astype(int)

    # Group by year and strand, summing the counts.
    grouped_df = FILTERED_DATA.groupby(['year', 'strand'], as_index=False)['counts'].sum()

    # Custom color palette
    custom_colors = ['#4F0A14', '#921224', '#D61B35', '#EA6074', '#F3A4AF']

    # Plotting the bar chart.
    seniorhigh_enrollment_comparison_per_strand = px.bar(
        grouped_df,
        x='year',
        y='counts',
        color='strand',
        barmode='group',
        labels={
            'year': 'Year',
            'counts': 'Number of Enrollees',
            'strand': 'Strands'
        },
        color_discrete_sequence=custom_colors
    )


    # Customize layout
    seniorhigh_enrollment_comparison_per_strand.update_layout(
        template='plotly_white',
        autosize=True,
        height=None,
        width=None,
        font=dict(color='#667889'),
        legend=dict(title='Strands', font=dict(color='#667889')),
        xaxis=dict(
            type='category',
            title_font=dict(color='#667889'),
            tickfont=dict(color='#667889')
        ),
        yaxis=dict(
            title_font=dict(color='#667889'),
            tickfont=dict(color='#667889')
        ),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    seniorhigh_enrollment_comparison_per_strand
    
    return dcc.Graph(figure=seniorhigh_enrollment_comparison_per_strand, config={"responsive": True}, style={"width": "100%", "height": "100%"})

##### HUMMS

@callback(
    Output('seniorhigh_humms', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    cleaned_df = FILTERED_DATA[FILTERED_DATA['strand'] != '__NaN__']
    cleaned_df['strand'] = cleaned_df['strand'].cat.remove_unused_categories()
    
    humms_df = cleaned_df[cleaned_df['strand'] == 'HUMSS']

    # Group data by year and gender
    grouped = humms_df.groupby(['year', 'gender'])['counts'].sum().reset_index()

    # Custom color map
    color_map = {
        'M': '#5DB7FF',
        'F': '#FF5B72'
    }


    # Create the area chart
    seniorhigh_humms = px.area(
        grouped,
        x='year',
        y='counts',
        color='gender',
        labels={
            'counts': 'Number of Enrollees',
            'year': 'Year',
            'gender': 'Gender'
        },
        color_discrete_map=color_map,
        category_orders={"year": sorted(grouped["year"].unique())}
    )


    # Update layout
    seniorhigh_humms.update_layout(
        template='plotly_white',
        autosize=True,
        font=dict(size=10, color="#667889", family="Inter, sans-serif"),
        margin=dict(l=5, r=5, t=5, b=5),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='right',
            x=1,
            title=None,
            font=dict(size=10, color="#667889")
        ),
        xaxis=dict(
            type='category',
            title=None,
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(color='#667889')
        ),
        yaxis=dict(
            title=None,
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(color='#667889')
        )
    )
    
    seniorhigh_humms.update_traces(
        mode='lines+markers',
        marker=dict(size=8),
        line=dict(width=3),
        # hovertemplate='<b>Year</b>: %{x}<br><b>Count</b>: %{y}<br><b>Level</b>: %{legendgroup}<extra></extra>'
    )


    seniorhigh_humms
    
    return dcc.Graph(figure=seniorhigh_humms, config={"responsive": True}, style={"width": "100%", "height": "100%"})

##### STEM

@callback(
    Output('seniorhigh_stem', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    cleaned_df = FILTERED_DATA[FILTERED_DATA['strand'] != '__NaN__']
    cleaned_df['strand'] = cleaned_df['strand'].cat.remove_unused_categories()
    
    stem_df = cleaned_df[cleaned_df['strand'] == 'STEM']

    # Group data by year and gender
    grouped = stem_df.groupby(['year', 'gender'])['counts'].sum().reset_index()

    # Custom color map
    color_map = {
        'M': '#5DB7FF',
        'F': '#FF5B72'
    }

    # Create the area chart
    seniorhigh_stem = px.area(
        grouped,
        x='year',
        y='counts',
        color='gender',
        labels={
            'counts': 'Number of Enrollees',
            'year': 'Year',
            'gender': 'Gender'
        },
        color_discrete_map=color_map,
        category_orders={"year": sorted(grouped["year"].unique())}
    )


    # Update layout
    seniorhigh_stem.update_layout(
        template='plotly_white',
        autosize=True,
        font=dict(size=10, color="#667889", family="Inter, sans-serif"),
        margin=dict(l=5, r=5, t=5, b=5),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.4,
            xanchor='right',
            x=1,
            title=None,
            font=dict(size=10, color="#667889")
        ),
        xaxis=dict(
            type='category',
            title=None,
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(color='#667889')
        ),
        yaxis=dict(
            title=None,
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(color='#667889')
        )
    )
    
    seniorhigh_stem.update_traces(
        mode='lines+markers',
        marker=dict(size=8),
        line=dict(width=3),
        # hovertemplate='<b>Year</b>: %{x}<br><b>Count</b>: %{y}<br><b>Level</b>: %{legendgroup}<extra></extra>'
    )


    seniorhigh_stem
    
    return dcc.Graph(figure=seniorhigh_stem, config={"responsive": True}, style={"width": "100%", "height": "100%"})

##### GAS

@callback(
    Output('seniorhigh_gas', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    cleaned_df = FILTERED_DATA[FILTERED_DATA['strand'] != '__NaN__']
    cleaned_df['strand'] = cleaned_df['strand'].cat.remove_unused_categories()
    
    gas_df = cleaned_df[cleaned_df['strand'] == 'GAS']

    # Group data by year and gender
    grouped = gas_df.groupby(['year', 'gender'])['counts'].sum().reset_index()

    # Custom color map
    color_map = {
        'M': '#5DB7FF',
        'F': '#FF5B72'
    }

    # Create the area chart
    seniorhigh_gas = px.area(
        grouped,
        x='year',
        y='counts',
        color='gender',
        labels={
            'counts': 'Number of Enrollees',
            'year': 'Year',
            'gender': 'Gender'
        },
        color_discrete_map=color_map,
        category_orders={"year": sorted(grouped["year"].unique())}
    )


    # Update layout
    seniorhigh_gas.update_layout(
        template='plotly_white',
        autosize=True,
        font=dict(size=10, color="#667889", family="Inter, sans-serif"),
        margin=dict(l=5, r=5, t=5, b=5),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.4,
            xanchor='right',
            x=1,
            title=None,
            font=dict(size=10, color="#667889")
        ),
        xaxis=dict(
            type='category',
            title=None,
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(color='#667889')
        ),
        yaxis=dict(
            title=None,
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(color='#667889')
        )
    )
    
    seniorhigh_gas.update_traces(
        mode='lines+markers',
        marker=dict(size=8),
        line=dict(width=3),
        # hovertemplate='<b>Year</b>: %{x}<br><b>Count</b>: %{y}<br><b>Level</b>: %{legendgroup}<extra></extra>'
    )


    seniorhigh_gas
    
    return dcc.Graph(figure=seniorhigh_gas, config={"responsive": True}, style={"width": "100%", "height": "100%"})

##### ABM

@callback(
    Output('seniorhigh_abm', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    cleaned_df = FILTERED_DATA[FILTERED_DATA['strand'] != '__NaN__']
    cleaned_df['strand'] = cleaned_df['strand'].cat.remove_unused_categories()
    
    abm_df = cleaned_df[cleaned_df['strand'] == 'ABM']

    # Group data by year and gender
    grouped = abm_df.groupby(['year', 'gender'])['counts'].sum().reset_index()

    # Custom color map
    color_map = {
        'M': '#5DB7FF',
        'F': '#FF5B72'
    }

    # Create the area chart
    seniorhigh_abm = px.area(
        grouped,
        x='year',
        y='counts',
        color='gender',
        labels={
            'counts': 'Number of Enrollees',
            'year': 'Year',
            'gender': 'Gender'
        },
        color_discrete_map=color_map,
        category_orders={"year": sorted(grouped["year"].unique())}
    )


    # Update layout
    seniorhigh_abm.update_layout(
        template='plotly_white',
        autosize=True,
        font=dict(size=10, color="#667889", family="Inter, sans-serif"),
        margin=dict(l=5, r=5, t=5, b=5),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.4,
            xanchor='right',
            x=1,
            title=None,
            font=dict(size=10, color="#667889")
        ),
        xaxis=dict(
            type='category',
            title=None,
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(color='#667889')
        ),
        yaxis=dict(
            title=None,
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(color='#667889')
        )
    )
    
    seniorhigh_abm.update_traces(
        mode='lines+markers',
        marker=dict(size=8),
        line=dict(width=3),
        # hovertemplate='<b>Year</b>: %{x}<br><b>Count</b>: %{y}<br><b>Level</b>: %{legendgroup}<extra></extra>'
    )


    seniorhigh_abm
    
    return dcc.Graph(figure=seniorhigh_abm, config={"responsive": True}, style={"width": "100%", "height": "100%"})

##### PBM

@callback(
    Output('seniorhigh_pbm', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    cleaned_df = FILTERED_DATA[FILTERED_DATA['strand'] != '__NaN__']
    cleaned_df['strand'] = cleaned_df['strand'].cat.remove_unused_categories()
    
    pbm_df = cleaned_df[cleaned_df['strand'] == 'PBM']

    # Group data by year and gender
    grouped = pbm_df.groupby(['year', 'gender'])['counts'].sum().reset_index()

    # Custom color map
    color_map = {
        'M': '#5DB7FF',
        'F': '#FF5B72'
    }

    # Create the area chart
    seniorhigh_pbm = px.area(
        grouped,
        x='year',
        y='counts',
        color='gender',
        labels={
            'counts': 'Number of Enrollees',
            'year': 'Year',
            'gender': 'Gender'
        },
        color_discrete_map=color_map,
        category_orders={"year": sorted(grouped["year"].unique())}
    )


    # Update layout
    seniorhigh_pbm.update_layout(
        template='plotly_white',
        autosize=True,
        font=dict(size=10, color="#667889", family="Inter, sans-serif"),
        margin=dict(l=5, r=5, t=5, b=5),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.4,
            xanchor='right',
            x=1,
            title=None,
            font=dict(size=10, color="#667889")
        ),
        xaxis=dict(
            type='category',
            title=None,
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(color='#667889')
        ),
        yaxis=dict(
            title=None,
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(color='#667889')
        )
    )
    
    seniorhigh_pbm.update_traces(
        mode='lines+markers',
        marker=dict(size=8),
        line=dict(width=3),
        # hovertemplate='<b>Year</b>: %{x}<br><b>Count</b>: %{y}<br><b>Level</b>: %{legendgroup}<extra></extra>'
    )


    seniorhigh_pbm
    
    return dcc.Graph(figure=seniorhigh_pbm, config={"responsive": True}, style={"width": "100%", "height": "100%"})
