import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State, Patch, html
from plotly.subplots import make_subplots 

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

# @callback(
#     Output('subclass_total_schools_per_subclass', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
#     # prevent_initial_call=True
# )
# def update_graph(trigger, data):
#     FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
#     FILTERED_DATA = FILTERED_DATA[['beis_id', 'sub_class', 'counts']]
    
#     subclass_df1 = (
#         FILTERED_DATA.groupby('sub_class')
#         .agg(
#             school_count=('beis_id', 'nunique'),
#             counts=('counts', 'sum'),  
#         )
#         .reset_index()
#     )

#     total_schools_per_subclass = px.bar(subclass_df1, 
#         x='school_count', 
#         y='sub_class',
#         labels={'sub_class': 'Subclass', 'school_count': 'Number of Schools'},
#         text='school_count',
#         color='sub_class',
#         color_discrete_sequence=['#012C53','#023F77','#02519B','#0264BE',
#                                 '#0377E2','#2991F1','#4FA4F3','#74B8F6','#9ACBF8'],
#     )
#     total_schools_per_subclass.update_xaxes(type='log')
#     total_schools_per_subclass.update_layout(
#         autosize=True,
#         margin={"l": 0, "r": 0, "t": 0, "b": 0},
#         yaxis=dict(showticklabels=True),
#         showlegend=False
#     )
        
#     return dcc.Graph(figure=total_schools_per_subclass)

# #################################################################################




# #################################################################################
# ##  --- Enrollment distribution by subclass
# #################################################################################

@callback(
    Output('subclass_distrib_by_subclass', 'children'),
    Output('others_subclass_distrib_by_subclass', 'children'),
    Output('sc-dist-tag', 'children'),
    Output('max-sc-dist', 'children'),
    Output('max-sc-dist-value', 'children'),
    Output('name-max-sc-dist', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):    
    # --- Filter & group data ---
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    FILTERED_DATA = FILTERED_DATA[['sector', 'sub_class', 'counts']]

    highlighted_classes = ['DepED Managed', 'Sectarian', 'Non-Sectarian']
    FILTERED_DATA['sub_class'] = FILTERED_DATA['sub_class'].astype('str')
    
    # Label others
    FILTERED_DATA['sub_class_grouped'] = FILTERED_DATA['sub_class'].apply(
        lambda x: x if x in highlighted_classes else 'Others'
    )
    
    # --- Main Pie Chart ---
    grouped_data = FILTERED_DATA.groupby('sub_class_grouped', as_index=False)['counts'].sum()
    
    total_counts = grouped_data['counts'].sum()

    # Identify top subclass and its percentage
    top_row = grouped_data.loc[grouped_data['counts'].idxmax()]
    top_subclass_name = top_row['sub_class_grouped']
    top_subclass_raw_pct = (top_row['counts'] / total_counts) * 100
    top_subclass_count = f"{int(top_row['counts']):,} Enrollees"

    if top_subclass_raw_pct >= 1:
        top_subclass_percentage = f"{round(top_subclass_raw_pct)}%"
    else:
        top_subclass_percentage = f"{top_subclass_raw_pct:.2f}%"

    main_pie = px.pie(
        grouped_data,
        values='counts',
        names='sub_class_grouped',
        color='sub_class_grouped',
        color_discrete_map={
            'DepED Managed': '#023F77',
            'Sectarian': '#9ACBF8',
            'Non-Sectarian': '#0377E2',
            'Others': '#CCCCCC'
        }
    )

    main_pie.update_traces(
        textinfo='label+percent',
        textfont_size=12,
        pull=[0.1 if x != 'DepED Managed' else 0 for x in grouped_data['sub_class_grouped']],
        marker=dict(line=dict(color='#FFFFFF', width=2)),
        rotation=45
    )

    main_pie.update_layout(
        title=None,
        autosize=True,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            title=None
        ),
        margin=dict(l=0, r=0, t=0, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # --- Bar Chart for "Others" ---
    total_counts = grouped_data['counts'].sum()
    others_data = FILTERED_DATA[FILTERED_DATA['sub_class_grouped'] == 'Others']
    others_grouped = others_data.groupby('sub_class', as_index=False)['counts'].sum()

    # Apply simplified naming
    simplified_labels = {
        'DOST Managed': 'DOST',
        'LUC Managed': 'LUC',
        'Local International School': 'Intl. Local',
        'Other GA Managed': 'Other Gov.',
        'School Abroad': 'Abroad',
        'SUC Managed': 'SUC',
        # Add more mappings if needed
    }
    others_grouped['sub_class'] = others_grouped['sub_class'].map(
        simplified_labels
    ).fillna(others_grouped['sub_class'])  # fallback if no match

    # Sort high to low
    others_grouped.sort_values(by='counts', ascending=True, inplace=True)

    others_count = grouped_data.loc[grouped_data['sub_class_grouped'] == 'Others', 'counts'].values[0]
    others_percentage = (others_count / total_counts) * 100
    
    if others_percentage >= 1:
        others_percentage_str = f"{round(others_percentage)}%"
    else:
        others_percentage_str = f"{others_percentage:.2f}%"


    others_bar = px.bar(
        others_grouped,
        x='counts',
        y='sub_class',
        orientation='h',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    others_bar.update_layout(
        title=None,
        showlegend=False,  
        autosize=True,
        margin=dict(l=15, r=15, t=20, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title='', automargin=True),
        xaxis=dict(title='Enrollment Count')
    )

    # --- Return both charts and percentage ---
    return (
        dcc.Graph(
            figure=main_pie,
            config={"responsive": True},
            style={"width": "100%", "height": "400px"}
        ),
        dcc.Graph(
            figure=others_bar,
            config={"responsive": True},
            style={"width": "100%", "height": "400px"}
        ),
        f"{others_percentage_str} Others",
        top_subclass_percentage,
        top_subclass_count,
        top_subclass_name
    )


# #################################################################################
# ##  --- Average enrollment per school
# #################################################################################

# @callback(
#     Output('subclass-enroll-dost', 'children'),
#     Output('subclass-enroll-deped', 'children'),
#     Output('subclass-enroll-luc', 'children'),
#     Output('subclass-enroll-int', 'children'),
#     Output('subclass-enroll-nonsec', 'children'),
#     Output('subclass-enroll-ga', 'children'),
#     Output('subclass-enroll-abroad', 'children'),
#     Output('subclass-enroll-suc', 'children'),
#     Output('subclass-enroll-sec', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
#     # prevent_initial_call=True
# )

# def update_graph(trigger, data):
#     FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
#     subclass_df2 = FILTERED_DATA.groupby(['sub_class','beis_id'], as_index=False)['counts'].sum()
#     avg_enrollment = subclass_df2.groupby('sub_class', as_index=False)['counts'].mean().round(0).astype({'counts': int})

#     def get_avg_enroll(subclass_name):
#         row = avg_enrollment.loc[avg_enrollment['sub_class'] == subclass_name, 'counts']
#         return row.values[0] if not row.empty else 0

#     avg_enroll_dost = get_avg_enroll('DOST Managed')
#     avg_enroll_deped = get_avg_enroll('DepED Managed')
#     avg_enroll_luc = get_avg_enroll('LUC Managed')
#     avg_enroll_int = get_avg_enroll('Local International School')
#     avg_enroll_nonsec = get_avg_enroll('Non-Sectarian')
#     avg_enroll_ga = get_avg_enroll('Other GA Managed')
#     avg_enroll_abroad = get_avg_enroll('School Abroad')
#     avg_enroll_suc = get_avg_enroll('SUC Managed')
#     avg_enroll_sec = get_avg_enroll('Sectarian')
    
#     return avg_enroll_dost, avg_enroll_deped, avg_enroll_luc, avg_enroll_int, avg_enroll_nonsec, avg_enroll_ga, avg_enroll_abroad, avg_enroll_suc, avg_enroll_sec

# #################################################################################



# #################################################################################
# ##  --- Student-to-school ratio
# #################################################################################

@callback(
    Output('subclass_student_school_ratio', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    subclass_df1 = (
        FILTERED_DATA.groupby('sub_class', observed=True)
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

    student_school_ratio.update_xaxes(
        type='log',
        showline=True,  # Show x-axis line
        linecolor='black',  # Color of the x-axis line
        linewidth=1  # Thickness of the x-axis line
    )

    student_school_ratio.update_yaxes(
        type='log',
        showline=True,  # Show y-axis line
        linecolor='black',  # Color of the y-axis line
        linewidth=1  # Thickness of the y-axis line
    )

    student_school_ratio.update_layout(
        xaxis_title='Number of Enrolled Students',
        yaxis_title='Number of Schools',
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        legend_title_text="",  # This removes the legend title
        legend={
            'orientation': 'h', 
            'yanchor': 'bottom',
            'y': -0.5, 
            'xanchor': 'center',
            'x': 0.5 
        },
        autosize=True,
        plot_bgcolor='rgba(0,0,0,0)',  # chart area transparent
        paper_bgcolor='rgba(0,0,0,0)',  # whole figure background transparent
    )
    
    return dcc.Graph(figure=student_school_ratio, config={"responsive": True}, style={"width": "100%", "height": "100%"})



# #################################################################################



# #################################################################################
# ##  --- Subclass vs school type
# #################################################################################

@callback(
    Output('subclass_vs_school_type', 'children'),
    Output('log-button-sc', 'children'),
    Input('chart-trigger', 'data'),
    Input('log-button-sc', 'n_clicks'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, n_clicks, data):
    # Apply smart filter
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)
    FILTERED_DATA = FILTERED_DATA[['beis_id', 'sub_class', 'type', 'mod_coc', 'counts']]
    
    # Check if the button is clicked an odd or even number of times
    if n_clicks % 2 == 0:
        xaxis_type = 'log'
        xaxis_tag = " Logarithm ▼ "
    else:
        xaxis_type = 'linear'
        xaxis_tag = " Linear ▼ "
    
    
    # Grouped DataFrames
    subclass_df1 = (
        FILTERED_DATA.groupby('sub_class', observed=True)
        .agg(
            school_count=('beis_id', 'nunique'),
            counts=('counts', 'sum'),
        )
        .reset_index()
        .sort_values('sub_class')
    )

    # Define custom order
    type_order = [
        "Mobile School",
        "Annex/Extension",
        "Mother School",
        "No Annexes"
    ]

    # Group and convert 'type' to ordered category
    df_by_type = (
        FILTERED_DATA.groupby(['sub_class', 'type'], observed=True)
        .agg(
            school_count=('beis_id', 'nunique'),
            counts=('counts', 'sum'),
        )
        .reset_index()
    )

    df_by_type['type'] = pd.Categorical(df_by_type['type'], categories=type_order, ordered=True)
    df_by_type = df_by_type.sort_values(['sub_class', 'type'])

    # Define desired mod_coc order
    modcoc_order = [
        "Purely SHS",
        "Purely JHS",
        "ES and JHS",
        "All Offering",
        "JHS with SHS",
        "Purely ES"
    ]

    # Group and convert 'mod_coc' to ordered category
    df_by_modcoc = (
        FILTERED_DATA.groupby(['sub_class', 'mod_coc'], observed=True)
        .agg(
            school_count=('beis_id', 'nunique'),
            counts=('counts', 'sum'),
        )
        .reset_index()
    )

    df_by_modcoc['mod_coc'] = pd.Categorical(df_by_modcoc['mod_coc'], categories=modcoc_order, ordered=True)
    df_by_modcoc = df_by_modcoc.sort_values(['sub_class', 'mod_coc'])

    # Initialize subplot: 1 row, 3 columns
    all_fig = make_subplots(
        rows=1, cols=3,
        shared_yaxes=True,
        horizontal_spacing=0.05,
        subplot_titles=("By School Type", "By Mode of Curriculum", "Total by Subclass")
    )

    # Chart 1: By type
    colors1 = ['#921224', '#D61B35', '#EA6074', '#F3A4AF']
    types = df_by_type['type'].unique()

    for i, t in enumerate(types):
        df_t = df_by_type[df_by_type['type'] == t].sort_values('sub_class')

        all_fig.add_trace(
            go.Bar(
                x=df_t['school_count'],
                y=df_t['sub_class'],
                orientation='h',
                name=t,
                marker_color=colors1[i % len(colors1)],
                showlegend=True
            ),
            row=1, col=1
        )

    # Chart 2: By mod_coc
    colors2 = [
        "#012C53",  # Purely SHS
        "#023F77",  # Purely JHS
        "#02519B",  # ES and JHS
        "#0377E2",  # All Offering
        "#4FA4F3",  # JHS with SHS
        "#9ACBF8",  # Purely ES
    ]

    modes = df_by_modcoc['mod_coc'].unique()

    for i, m in enumerate(modes):
        df_m = df_by_modcoc[df_by_modcoc['mod_coc'] == m].sort_values('sub_class')

        all_fig.add_trace(
            go.Bar(
                x=df_m['school_count'],
                y=df_m['sub_class'],
                orientation='h',
                name=m,
                marker_color=colors2[i % len(colors2)],
                showlegend=True  # hide legend to reduce clutter
            ),
            row=1, col=2
        )

    # Chart 3: Total, solid color
    all_fig.add_trace(
        go.Bar(
            x=subclass_df1['school_count'],
            y=subclass_df1['sub_class'],
            orientation='h',
            text=subclass_df1['school_count'],
            name="Total",
            marker_color="#023f77",
            showlegend=False
        ),
        row=1, col=3
    )

    # Set log x-axis
    for col in [1, 2, 3]:
        all_fig.update_xaxes(type=xaxis_type, row=1, col=col)

    # Layout
    for col in [1, 2, 3]:
        all_fig.update_xaxes(
            showline=True,
            linecolor='#4F0A14',  # or '#667889'
            linewidth=1,
            showgrid=False,
            zeroline=False,
            ticks="outside",
            row=1, col=col
        )
    
    all_fig.update_layout(
        xaxis=dict(
            showline=True,
            linecolor='black',   # or any visible color like '#667889'
            linewidth=1          # optional, default is 1
        ),
        annotations=[
            dict(
                text="Number of School",
                x=0.5, y=-0.15,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=14, color="#667889"),
                xanchor='center'
            )
        ],
        barmode='stack',
        legend=dict(
            # title={'text': "Legend", 'font': {'color': '#667889'}},
            font={'color': '#667889'},
            orientation='h',
            yanchor='bottom',
            y=-0.35,
            xanchor='center',
            x=0.5
        ),
        margin=dict(l=10, r=10, t=30, b=40),
        autosize=True,
        plot_bgcolor='rgba(0,0,0,0)',  # chart area transparent
        paper_bgcolor='rgba(0,0,0,0)',  # whole figure background transparent
    )

    # Return in Dash
    return dcc.Graph(figure=all_fig, config={"responsive": True}, style={"width": "100%", "height": "100%"}), xaxis_tag
        
    
    

# #################################################################################



# #################################################################################
# ##  --- Sector affiliation
# #################################################################################

@callback(
    Output('subclass_sector_affiliation', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    subclass_df4 = FILTERED_DATA.groupby(['sub_class', 'sector'], observed=True).agg(
        school_count=('beis_id', 'nunique'),
        total_enrollees=('counts', 'sum')
    ).reset_index()

    # Filter out rows with zero values
    subclass_df4 = subclass_df4[(subclass_df4['school_count'] > 0) & (subclass_df4['total_enrollees'] > 0)]

    # Sort by total enrollees
    subclass_df4.sort_values(by='total_enrollees', ascending=False, inplace=True)

    # Replace long category name
    subclass_df4['sub_class'] = subclass_df4['sub_class'].astype(str).str.replace(
        'Local International School', 'Local Intl. School'
    )

    # Format school_count and total_enrollees with comma separators
    subclass_df4['school_count'] = subclass_df4['school_count'].apply(lambda x: f"{x:,}")
    subclass_df4['total_enrollees'] = subclass_df4['total_enrollees'].apply(lambda x: f"{x:,}")

    sector_affiliation = go.Figure(data=[go.Table(
        header=dict(
            values=["Subclass", "Sector", "No. of Schools", "Total Enrollees"],
            fill_color='#EA6074',
            align='left',
            font=dict(size=12),
            line=dict(width=1),
            height=40
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
            font=dict(size=12),
            line=dict(width=1),
            height=35
        )
    )])

    sector_affiliation.update_layout(
        height=400,
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return dcc.Graph(
        figure=sector_affiliation,
        config={"responsive": True},
        style={"width": "100%", "height": "400px"}
    )

    
# #################################################################################



# #################################################################################
# ##  --- Regional distribution/ which subclass has the highest number of schools per loc
# #################################################################################

# @callback(
#     Output('subclass_heatmap', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
#     # prevent_initial_call=True
# )

# def update_graph(trigger, data):
#     FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
#     # Assuming FILTERED_DF is already defined
#     query2 = FILTERED_DATA[['region', 'sub_class']][:]

#     # Count the number of schools per sub_class per region
#     query2 = query2.groupby(['region', 'sub_class']).size().reset_index(name='school_count')

#     # Pivot the data to wide format for heatmap
#     heatmap_df = query2.pivot(index='region', columns='sub_class', values='school_count').fillna(0)

#     # Reset index for Plotly compatibility
#     heatmap_df = heatmap_df.reset_index().melt(id_vars='region', var_name='sub_class', value_name='school_count')

#     # Create heatmap with custom reversed secondary shades palette
#     subclass_heatmap = px.density_heatmap(
#         heatmap_df,
#         x='sub_class',
#         y='region',
#         z='school_count',
#         color_continuous_scale=[
#             '#F3A4AF',  # Lightest - secondary-shades-9
#             '#EF8292',
#             '#EA6074',
#             '#E63E56',
#             '#D61B35',
#             '#B4162D',
#             '#921224',
#             '#710E1C',
#             '#4F0A14'   # Darkest - secondary-shades-1
#         ],
#         text_auto=False
#     )

#     # Update layout for improved visuals
#     subclass_heatmap.update_layout(
#         xaxis=dict(
#             tickangle=45,
#             tickfont=dict(size=9),
#             title=''
#         ),
#         yaxis=dict(
#             tickfont=dict(size=9),
#             title='',
#         ),
#         coloraxis_colorbar=dict(
#             title=dict(
#                 text='Schools',
#                 font=dict(
#                     family='Inter Medium',
#                     size=10
#                 )
#             )
#         ),
#         font=dict(size=11),
#         autosize=True,
#         margin={"l": 100, "r": 10, "t": 40, "b": 50}
#     )
    
#     return dcc.Graph(figure=subclass_heatmap)


# #################################################################################

    


# #################################################################################
# ##  --- MCOC breakdown/which subclass offers which program types
# #################################################################################

# @callback(
#     Output('subclass_clustered', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
#     # prevent_initial_call=True
# )

# # def update_graph(trigger, data):
# #     FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
# #     # Ensure the dataframe is filtered to include only the required columns
# #     mcoc_df = FILTERED_DATA[['mod_coc', 'counts', 'sub_class']]

# #     # Group by 'mod_coc' and 'sub_class' to aggregate the counts
# #     mcoc_grouped = mcoc_df.groupby(['mod_coc', 'sub_class']).sum().reset_index()

# #     # Capitalize each word in 'sub_class' for the legend
# #     mcoc_grouped['sub_class'] = mcoc_grouped['sub_class'].str.title()

# #     # Revert the counts back to numeric for plotting
# #     mcoc_grouped['counts_numeric'] = mcoc_grouped['counts'].apply(
# #         lambda count: float(count.replace('M', 'e6').replace('K', 'e3')) if isinstance(count, str) else count
# #     )

# #     # Create the clustered bar chart
# #     subclass_clustered = px.bar(
# #         mcoc_grouped,
# #         x='mod_coc',
# #         y='counts_numeric',
# #         color='sub_class',
# #         title='Course Offerings',
# #         labels={'counts_numeric': '', 'mod_coc': 'mod_coc'},
# #         category_orders={'sub_class': sorted(mcoc_grouped['sub_class'].unique())},
# #         barmode='group'
# #     )

# #     # Customize the layout further using update_layout
# #     subclass_clustered.update_layout(
# #         title="Clustered Bar Chart for mod_coc vs. Sub_Class",
# #         xaxis=dict(
# #             title="mod_coc",  # Label for the x-axis
# #             tickangle=45,  # Rotate x-axis ticks for better readability
# #             tickmode='array',
# #             tickvals=mcoc_grouped['mod_coc'].unique(),  # Ensure all mod_coc values are shown
# #         ),
# #         yaxis=dict(
# #             title="Counts (in millions or thousands)",  # Label for the y-axis
# #             tickformat=".1f",  # Format y-axis ticks to show one decimal place
# #         ),
# #         legend_title="Sub Class",  # Title for the legend
# #         barmode='group',  # Ensure bars are grouped
# #         margin=dict(l=50, r=50, t=50, b=100),  # Set margins for the chart for better spacing
# #     )

# #     return dcc.Graph(figure=subclass_clustered)

# def update_graph(trigger, data):
#     FILTERED_DATA = smart_filter(data, enrollment_db_engine)

#     # Filter to necessary columns
#     mcoc_df = FILTERED_DATA[['mod_coc', 'sub_class', 'beis_id']]

#     # Capitalize and truncate for clean labels
#     mcoc_df['sub_class'] = mcoc_df['sub_class'].str.title().str.slice(0, 15)
#     mcoc_df['mod_coc'] = mcoc_df['mod_coc'].str.slice(0, 20)

#     # Count unique 'beis_id' per (mod_coc, sub_class) to get the number of schools
#     mcoc_grouped = (
#         mcoc_df.groupby(['mod_coc', 'sub_class'])
#         .agg(school_count=('beis_id', 'nunique'))  # Count unique schools (beis_id)
#         .reset_index()
#     )

#     # Get top 3 sub_classes by total school count
#     top_subclasses = (
#         mcoc_grouped.groupby('sub_class')['school_count']
#         .sum()
#         .nlargest(3)
#         .index
#     )

#     # Filter to top 3 only
#     mcoc_grouped = mcoc_grouped[mcoc_grouped['sub_class'].isin(top_subclasses)]

#     # Create the horizontal bar chart
#     subclass_clustered = px.bar(
#         mcoc_grouped,
#         x='school_count',
#         y='mod_coc',
#         color='sub_class',
#         title='Number of Schools per Course Offering',
#         labels={'school_count': 'Number of Schools', 'mod_coc': 'Course Offering'},
#         category_orders={'sub_class': sorted(top_subclasses)},
#         barmode='group',
#         orientation='h'
#     )

#     subclass_clustered.update_xaxes(type='log')
    
#     # Update layout with shortened counts (using SI format like 1k)
#     subclass_clustered.update_layout(
#         title="Course Offerings by Subclass",
#         title_font=dict(family='Inter Bold', size=14, color='#04508c'),
#         xaxis=dict(
#             title="Number of Schools",
#             tickformat="~s",  
#         ),
#         yaxis=dict(
#             title="Course Offering",
#             categoryorder='total ascending',
#         ),
#         legend_title="Top Subclass",
#         legend_title_font=dict(family='Inter Semi Bold', size=13, color='#667889'),
#         margin=dict(l=100, r=50, t=50, b=50),
#     )

#     return dcc.Graph(figure=subclass_clustered)








# #################################################################################



# #################################################################################
# ##  --- Enrollment in shs tracks across subclass
# #################################################################################

@callback(
    Output('subclass_clustered_tracks', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

# def update_graph(trigger, data):
#     FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
#     # Filter the dataframe to include only SHS tracks and subclasses
#     shs_tracks_df = FILTERED_DATA[['track', 'sub_class']]

#     # Remove rows with missing values in 'track' or 'sub_class'
#     shs_tracks_df = shs_tracks_df.dropna(subset=['track', 'sub_class'])

#     # Group by 'track' and 'sub_class' and count the entries
#     shs_tracks_grouped = shs_tracks_df.groupby(['track', 'sub_class']).size().reset_index(name='counts')

#     # Capitalize each word in 'sub_class' for the legend
#     shs_tracks_grouped['sub_class'] = shs_tracks_grouped['sub_class'].str.title()

#     # Truncate 'track' and 'sub_class' values for better readability
#     shs_tracks_grouped['track'] = shs_tracks_grouped['track'].str.slice(0, 20)
#     shs_tracks_grouped['sub_class'] = shs_tracks_grouped['sub_class'].str.slice(0, 15)

#     # Create a clustered bar chart for SHS tracks and subclasses
#     subclass_clustered_tracks = px.bar(
#         shs_tracks_grouped,
#         x='track',
#         y='counts',
#         color='sub_class',
#         barmode='group',
#         title='Enrollment in SHS Tracks Across Subclass'
#     )

#     # Update chart layout for improved readability
#     subclass_clustered_tracks.update_layout(
#         title=dict(
#             text='SHS Tracks Enrollment',
#             font=dict(family='Inter Bold', size=14, color='#04508c'),
#             x=0  # Left align the title
#         ),
#         xaxis=dict(
#             title='',
#             tickangle=45,
#             tickfont=dict(size=10, family='Inter Medium')
#         ),
#         yaxis=dict(
#             title='',
#             tickfont=dict(size=10, family='Inter Medium')
#         ),
#         showlegend=True,  # Display legend for clarity
#         legend_title=None,  # Remove legend title (sub_class)
#         font=dict(size=11, family='Inter Medium'),
#         autosize=True,
#         margin={"l": 50, "r": 10, "t": 50, "b": 40}  # Adjust margins
#     )
        
#     return dcc.Graph(figure=subclass_clustered_tracks)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    # Keep only necessary columns and drop rows with missing values
    shs_tracks_df = FILTERED_DATA[['track', 'sub_class']].dropna(subset=['track', 'sub_class'])

    # Group by 'track' and 'sub_class', then count enrollments
    shs_tracks_grouped = (
        shs_tracks_df
        .groupby(['track', 'sub_class'])
        .size()
        .reset_index(name='enrollment_count')
    )

    # Capitalize and truncate for readability
    shs_tracks_grouped['track'] = shs_tracks_grouped['track'].str.slice(0, 20)
    shs_tracks_grouped['sub_class'] = shs_tracks_grouped['sub_class'].str.title().str.slice(0, 15)

    # Create the clustered bar chart
    subclass_clustered_tracks = px.bar(
        shs_tracks_grouped,
        x='track',
        y='enrollment_count',
        color='sub_class',
        barmode='group',
        title='SHS Tracks Enrollment by Subclass'
    )

    # Update layout for clarity and short number formatting
    subclass_clustered_tracks.update_layout(
        title=dict(
            text='SHS Tracks Enrollment',
            font=dict(family='Inter Bold', size=14, color='#04508c'),
            x=0  # Left-align the title
        ),
        xaxis=dict(
            title='',
            tickangle=45,
            tickfont=dict(size=10, family='Inter Medium')
        ),
        yaxis=dict(
            title='Enrollment Count',
            tickfont=dict(size=10, family='Inter Medium'),
            tickformat='~s'  
        ),
        showlegend=True,
        legend_title=None,
        font=dict(size=11, family='Inter Medium'),
        autosize=True,
        margin={"l": 50, "r": 10, "t": 50, "b": 40}
    )

    return dcc.Graph(figure=subclass_clustered_tracks)





# #################################################################################


# #################################################################################
# ##  --- % schools offering ‘all offerings’ for the entire mod_coc
# #################################################################################

# @callback(
#     Output('top_offering_subclass', 'children'),
#     Output('top_offering_percentage', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
#     # prevent_initial_call=True
# )

# def update_graph(trigger, data):
#     FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
#     # Total schools per subclass
#     total_counts = FILTERED_DATA.groupby('sub_class')['counts'].sum()

#     # Schools offering "All Offering" per subclass
#     all_offerings_counts = FILTERED_DATA[FILTERED_DATA['mod_coc'] == 'All Offering'].groupby('sub_class')['counts'].sum()

#     # Compute % of All Offering per subclass, drop NaNs (where no offering exists)
#     percentage_per_subclass = ((all_offerings_counts / total_counts) * 100).dropna().round(2)

#     # Helper function to get percentage by subclass
#     def get_offering_percentage(subclass_name):
#         return percentage_per_subclass.get(subclass_name, None)

#     # Get top subclass and its percentage
#     top_offering_subclass = percentage_per_subclass.idxmax()
#     top_offering_percentage = percentage_per_subclass.max()
    
#     return top_offering_subclass, f"{top_offering_percentage}%"

# #################################################################################



# #################################################################################
# ##  --- % schools offering shs per subclass
# #################################################################################

# @callback(
#     Output('top_track_subclass', 'children'),
#     Output('top_track_percentage', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
#     # prevent_initial_call=True
# )

# def update_graph(trigger, data):
#     FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
#     # Get all unique SHS tracks
#     unique_tracks = FILTERED_DATA['track'].dropna().unique()
#     total_tracks = len(unique_tracks)

#     # Count the unique tracks offered per subclass
#     tracks_per_subclass = FILTERED_DATA.groupby('sub_class')['track'].nunique()

#     # Calculate percentage per subclass
#     percentage_tracks_per_subclass = ((tracks_per_subclass / total_tracks) * 100).dropna().round(2)

#     # Helper function to retrieve % of SHS track coverage by subclass
#     def get_track_coverage(subclass_name):
#         return percentage_tracks_per_subclass.get(subclass_name, None)

#     # Get top-performing subclass and its percentage
#     top_track_subclass = percentage_tracks_per_subclass.idxmax()
#     top_track_percentage = percentage_tracks_per_subclass.max()
        
#     return top_track_subclass, f"{top_track_percentage}%"


# #################################################################################