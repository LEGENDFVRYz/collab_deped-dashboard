import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State, Patch

# important part
from src.data import enrollment_db_engine, smart_filter

# # from utils.reports.location_chart import FILTERED_DF

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# from config import project_root
# from utils.get_data import auto_extract

# """
#     Analytics/SHS Tracks and Strands Charts and Indicator
# """

# #################################################################################
# ##                     MAIN DATAFRAME BASED FROM THE QUERY                     ##
# #################################################################################

# ## -- FIND YOUR CHARTS HERE:

# ################################################################################
# ##  --- Total schools per subclass
# #################################################################################

@callback(
    Output('subclass_total_schools_per_subclass', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    subclass_df1 = (
        FILTERED_DATA.groupby('sub_class')
        .agg(
            school_count=('beis_id', 'nunique'),
            counts=('counts', 'sum'),  
        )
        .reset_index()
    )

    total_schools_per_subclass = px.bar(subclass_df1, 
        x='school_count', 
        y='sub_class',
        labels={'sub_class': 'Subclass', 'school_count': 'Number of Schools'},
        text='school_count',
        color='sub_class',
        color_discrete_sequence=['#012C53','#023F77','#02519B','#0264BE',
                                '#0377E2','#2991F1','#4FA4F3','#74B8F6','#9ACBF8'],
    )
    
    total_schools_per_subclass.update_layout(
        autosize=True,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        yaxis=dict(showticklabels=True),
        showlegend=False
    )
        
    return dcc.Graph(figure=total_schools_per_subclass)

# #################################################################################




# #################################################################################
# ##  --- Enrollment distribution by subclass
# #################################################################################

@callback(
    Output('subclass_distrib_by_subclass', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    distrib_by_subclass = px.pie(FILTERED_DATA, 
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
        textfont_size=7,
        pull=[0.1 if x != 'DepED Managed' else 0 for x in FILTERED_DATA['sub_class']],
        marker=dict(line=dict(color='#FFFFFF', width=2)),
        rotation=45
    )
    
    distrib_by_subclass.update_layout(
        autosize=True,
        showlegend=True,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )
    
    return dcc.Graph(figure=distrib_by_subclass)

# #################################################################################
# ##  --- Average enrollment per school
# #################################################################################

@callback(
    Output('subclass-enroll-dost', 'children'),
    Output('subclass-enroll-deped', 'children'),
    Output('subclass-enroll-luc', 'children'),
    Output('subclass-enroll-int', 'children'),
    Output('subclass-enroll-nonsec', 'children'),
    Output('subclass-enroll-ga', 'children'),
    Output('subclass-enroll-abroad', 'children'),
    Output('subclass-enroll-suc', 'children'),
    Output('subclass-enroll-sec', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    subclass_df2 = FILTERED_DATA.groupby(['sub_class','beis_id'], as_index=False)['counts'].sum()
    avg_enrollment = subclass_df2.groupby('sub_class', as_index=False)['counts'].mean().round(0).astype({'counts': int})

    def get_avg_enroll(subclass_name):
        row = avg_enrollment.loc[avg_enrollment['sub_class'] == subclass_name, 'counts']
        return row.values[0] if not row.empty else 0

    avg_enroll_dost = get_avg_enroll('DOST Managed')
    avg_enroll_deped = get_avg_enroll('DepED Managed')
    avg_enroll_luc = get_avg_enroll('LUC Managed')
    avg_enroll_int = get_avg_enroll('Local International School')
    avg_enroll_nonsec = get_avg_enroll('Non-Sectarian')
    avg_enroll_ga = get_avg_enroll('Other GA Managed')
    avg_enroll_abroad = get_avg_enroll('School Abroad')
    avg_enroll_suc = get_avg_enroll('SUC Managed')
    avg_enroll_sec = get_avg_enroll('Sectarian')
    
    return avg_enroll_dost, avg_enroll_deped, avg_enroll_luc, avg_enroll_int, avg_enroll_nonsec, avg_enroll_ga, avg_enroll_abroad, avg_enroll_suc, avg_enroll_sec

# #################################################################################



# #################################################################################
# ##  --- Student-to-school ratio
# #################################################################################

@callback(
    Output('subclass_student_school_ratio', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    subclass_df1 = (
        FILTERED_DATA.groupby('sub_class')
        .agg(
            school_count=('beis_id', 'nunique'),
            counts=('counts', 'sum'),  
        )
        .reset_index()
    )
    
    student_school_ratio = px.scatter(subclass_df1, 
        x="counts", 
        y="school_count",
        color='sub_class',
        color_discrete_sequence=['#012C53','#023F77','#02519B','#0264BE',
                                '#0377E2','#2991F1','#4FA4F3','#74B8F6','#9ACBF8'],
    )
    student_school_ratio.update_traces(marker=dict(size=12))
    student_school_ratio.update_layout(
        xaxis_title='Number of Enrolled Students',
        yaxis_title='Number of Schools',
        margin={"l": 0, "r": 0, "t": 0, "b": 50},
        scattermode="group",
        legend={
            'title': {'text': "Subclassifications", 'font': {'color': '#667889'}},
            'orientation': 'h', 
            'yanchor': 'bottom',
            'y': -20, 
            'xanchor': 'left',
            'x': 0.5 
        }
    )
    
    return dcc.Graph(figure=student_school_ratio)

# #################################################################################



# #################################################################################
# ##  --- Subclass vs school type
# #################################################################################

@callback(
    Output('subclass_vs_school_type', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    subclass_df3 = (
        FILTERED_DATA.groupby(['sub_class','type'])
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
            'xanchor': 'left',
            'x': 0.5 
        },
        margin=dict(l=0, r=0, t=0, b=40),
        autosize=True,
        #width=600,
    )
    subclass_vs_school_type
    
    return dcc.Graph(figure=subclass_vs_school_type)

# #################################################################################



# #################################################################################
# ##  --- Sector affiliation
# #################################################################################

@callback(
    Output('subclass_sector_affiliation', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    subclass_df4 = FILTERED_DATA.groupby(['sub_class', 'sector']).agg(
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
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )
    
    return dcc.Graph(figure=sector_affiliation)

# #################################################################################



# #################################################################################
# ##  --- Regional distribution/ which subclass has the highest number of schools per loc
# #################################################################################

@callback(
    Output('subclass_heatmap', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Assuming FILTERED_DF is already defined
    query2 = FILTERED_DATA[['region', 'sub_class']][:]

    # Count the number of schools per sub_class per region
    query2 = query2.groupby(['region', 'sub_class']).size().reset_index(name='school_count')

    # Pivot the data to wide format for heatmap
    heatmap_df = query2.pivot(index='region', columns='sub_class', values='school_count').fillna(0)

    # Reset index for Plotly compatibility
    heatmap_df = heatmap_df.reset_index().melt(id_vars='region', var_name='sub_class', value_name='school_count')

    # Create heatmap with custom reversed secondary shades palette
    subclass_heatmap = px.density_heatmap(
        heatmap_df,
        x='sub_class',
        y='region',
        z='school_count',
        color_continuous_scale=[
            '#F3A4AF',  # Lightest - secondary-shades-9
            '#EF8292',
            '#EA6074',
            '#E63E56',
            '#D61B35',
            '#B4162D',
            '#921224',
            '#710E1C',
            '#4F0A14'   # Darkest - secondary-shades-1
        ],
        text_auto=False
    )

    # Update layout for improved visuals
    subclass_heatmap.update_layout(
        title=dict(
            text='Regional Distribution of Schools',
            font=dict(
                family='Inter Bold',
                size=14,
                color='#04508c'
            )
        ),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=9),
            title=''
        ),
        yaxis=dict(
            tickfont=dict(size=9),
            title='',
        ),
        coloraxis_colorbar=dict(
            title=dict(
                text='Schools',
                font=dict(
                    family='Inter Medium',
                    size=10
                )
            )
        ),
        font=dict(size=11),
        autosize=True,
        margin={"l": 100, "r": 10, "t": 40, "b": 50}
    )
    
    return dcc.Graph(figure=subclass_heatmap)


# #################################################################################



# #################################################################################
# ##  --- MCOC breakdown/which subclass offers which program types
# #################################################################################

@callback(
    Output('subclass_clustered', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Ensure the dataframe is filtered to include only the required columns
    mcoc_df = FILTERED_DATA[['mod_coc', 'counts', 'sub_class']]

    # Group by 'mod_coc' and 'sub_class' to aggregate the counts
    mcoc_grouped = mcoc_df.groupby(['mod_coc', 'sub_class']).sum().reset_index()

    # Capitalize each word in 'sub_class' for the legend
    mcoc_grouped['sub_class'] = mcoc_grouped['sub_class'].str.title()

    # Revert the counts back to numeric for plotting
    mcoc_grouped['counts_numeric'] = mcoc_grouped['counts'].apply(
        lambda count: float(count.replace('M', 'e6').replace('K', 'e3')) if isinstance(count, str) else count
    )

    # Create the clustered bar chart
    subclass_clustered = px.bar(
        mcoc_grouped,
        x='mod_coc',
        y='counts_numeric',
        color='sub_class',
        title='Clustered Bar Chart for mod_coc vs. Sub_Class',
        labels={'counts_numeric': 'Counts (in millions or thousands)', 'mod_coc': 'mod_coc'},
        category_orders={'sub_class': sorted(mcoc_grouped['sub_class'].unique())},
        barmode='group'
    )

    # Customize the layout further using update_layout
    subclass_clustered.update_layout(
        title="Clustered Bar Chart for mod_coc vs. Sub_Class",
        xaxis=dict(
            title="mod_coc",  # Label for the x-axis
            tickangle=45,  # Rotate x-axis ticks for better readability
            tickmode='array',
            tickvals=mcoc_grouped['mod_coc'].unique(),  # Ensure all mod_coc values are shown
        ),
        yaxis=dict(
            title="Counts (in millions or thousands)",  # Label for the y-axis
            tickformat=".1f",  # Format y-axis ticks to show one decimal place
        ),
        legend_title="Sub Class",  # Title for the legend
        barmode='group',  # Ensure bars are grouped
        margin=dict(l=50, r=50, t=50, b=100),  # Set margins for the chart for better spacing
    )

    return dcc.Graph(figure=subclass_clustered)

# #################################################################################



# #################################################################################
# ##  --- Enrollment in shs tracks across subclass
# #################################################################################

@callback(
    Output('subclass_clustered_tracks', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Filter the dataframe to include only SHS tracks and subclasses
    shs_tracks_df = FILTERED_DATA[['track', 'sub_class']]

    # Remove rows with missing values in 'track' or 'sub_class'
    shs_tracks_df = shs_tracks_df.dropna(subset=['track', 'sub_class'])

    # Group by 'track' and 'sub_class' and count the entries
    shs_tracks_grouped = shs_tracks_df.groupby(['track', 'sub_class']).size().reset_index(name='counts')

    # Capitalize each word in 'sub_class' for the legend
    shs_tracks_grouped['sub_class'] = shs_tracks_grouped['sub_class'].str.title()

    # Truncate 'track' and 'sub_class' values for better readability
    shs_tracks_grouped['track'] = shs_tracks_grouped['track'].str.slice(0, 20)
    shs_tracks_grouped['sub_class'] = shs_tracks_grouped['sub_class'].str.slice(0, 15)

    # Create a clustered bar chart for SHS tracks and subclasses
    subclass_clustered_tracks = px.bar(
        shs_tracks_grouped,
        x='track',
        y='counts',
        color='sub_class',
        barmode='group',
        title='Enrollment in SHS Tracks Across Subclass'
    )

    # Update chart layout for improved readability
    subclass_clustered_tracks.update_layout(
        title=dict(
            text='SHS Tracks Enrollment',
            font=dict(family='Inter Bold', size=14, color='#04508c'),
            x=0  # Left align the title
        ),
        xaxis=dict(
            title='',
            tickangle=45,
            tickfont=dict(size=10, family='Inter Medium')
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=10, family='Inter Medium')
        ),
        showlegend=True,  # Display legend for clarity
        legend_title=None,  # Remove legend title (sub_class)
        font=dict(size=11, family='Inter Medium'),
        autosize=True,
        margin={"l": 50, "r": 10, "t": 50, "b": 40}  # Adjust margins
    )
        
    return dcc.Graph(figure=subclass_clustered_tracks)


# #################################################################################


# #################################################################################
# ##  --- % schools offering ‘all offerings’ for the entire mod_coc
# #################################################################################

@callback(
    Output('top_offering_subclass', 'children'),
    Output('top_offering_percentage', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Total schools per subclass
    total_counts = FILTERED_DATA.groupby('sub_class')['counts'].sum()

    # Schools offering "All Offering" per subclass
    all_offerings_counts = FILTERED_DATA[FILTERED_DATA['mod_coc'] == 'All Offering'].groupby('sub_class')['counts'].sum()

    # Compute % of All Offering per subclass, drop NaNs (where no offering exists)
    percentage_per_subclass = ((all_offerings_counts / total_counts) * 100).dropna().round(2)

    # Helper function to get percentage by subclass
    def get_offering_percentage(subclass_name):
        return percentage_per_subclass.get(subclass_name, None)

    # Get top subclass and its percentage
    top_offering_subclass = percentage_per_subclass.idxmax()
    top_offering_percentage = percentage_per_subclass.max()
    
    return top_offering_subclass, f"{top_offering_percentage}%"

# #################################################################################



# #################################################################################
# ##  --- % schools offering shs per subclass
# #################################################################################

@callback(
    Output('top_track_subclass', 'children'),
    Output('top_track_percentage', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Get all unique SHS tracks
    unique_tracks = FILTERED_DATA['track'].dropna().unique()
    total_tracks = len(unique_tracks)

    # Count the unique tracks offered per subclass
    tracks_per_subclass = FILTERED_DATA.groupby('sub_class')['track'].nunique()

    # Calculate percentage per subclass
    percentage_tracks_per_subclass = ((tracks_per_subclass / total_tracks) * 100).dropna().round(2)

    # Helper function to retrieve % of SHS track coverage by subclass
    def get_track_coverage(subclass_name):
        return percentage_tracks_per_subclass.get(subclass_name, None)

    # Get top-performing subclass and its percentage
    top_track_subclass = percentage_tracks_per_subclass.idxmax()
    top_track_percentage = percentage_tracks_per_subclass.max()
        
    return top_track_subclass, f"{top_track_percentage}%"


# #################################################################################