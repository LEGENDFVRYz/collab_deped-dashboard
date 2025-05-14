import time
from turtle import title
from unicodedata import category
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State, Patch

# important part
from src.data import enrollment_db_engine, smart_filter
from src.utils.extras_utils import smart_truncate_number

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# from config import project_root
# from utils.get_data import auto_extract


# """
#     Analytics/Offering Charts and Indicator
    
# """


# #################################################################################
# ##                     MAIN DATAFRAME BASED FROM THE QUERY                     ##
# #################################################################################

# # ## -- This only a temporary dataframe for testing your charts, you can change it
# FILTERED_DF = dataframe = auto_extract(['counts'], is_specific=False)
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
# # sample_chart.update_layout(
# #     autosize=True,
# #     margin={"l": 8, "r": 8, "t": 12, "b": 8},  # Optional: Adjust margins
# # )
# sample_chart

# #################################################################################
# #################################################################################




# ## -- FIND YOUR CHARTS HERE:

# #################################################################################
# ##  --- CHART: Number of Schools by MCOC Type
# #################################################################################

@callback(
    Output('offering_number-of-schools', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # Extract and group
    grouped_by_offering = FILTERED_DATA.groupby("mod_coc")['beis_id'].nunique().reset_index(name="counts")
    
    # Drop duplicate schools
    cleaned_FILTERED_DF = FILTERED_DATA.drop_duplicates(subset='beis_id')
    
    # total_school_count = len(cleaned_FILTERED_DF)
    # shs_percentage = f"{(shs_total / total_school_count * 100):.1f}%" if total_school_count else "0%"

    # Order inner donut
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

    grouped_by_offering['mod_coc'] = pd.Categorical(
        grouped_by_offering['mod_coc'], categories=desired_order, ordered=True
    )
    grouped_by_offering = grouped_by_offering.sort_values('mod_coc')

    inner_labels = grouped_by_offering['mod_coc']
    inner_values = grouped_by_offering['counts']
    inner_colors = inner_labels.map(inner_color_map)
    
    number_of_schools_mcoc_chart = go.Figure()
    
    number_of_schools_mcoc_chart.add_trace(go.Pie(
        labels=inner_labels,
        values=inner_values,
        hole=0.43,
        direction='clockwise',
        rotation=90,
        sort=False,
        textinfo='none',
        marker=dict(colors=inner_colors, line=dict(color='#3C6382', width=0)),
        domain={'x': [0,1], 'y': [0,1]},
        name='Level',
        legendgroup='Education Level',
    ))

    # Layout
    number_of_schools_mcoc_chart.update_layout(
        showlegend=False,
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(
            orientation='h',        # horizontal legend
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5                   # center horizontally
        )
    )
    
    number_of_schools_mcoc_chart

    # number_of_schools_mcoc = FILTERED_DATA.groupby('mod_coc')['beis_id'].nunique().reset_index()
    # number_of_schools_mcoc.rename(columns={'beis_id': 'school_count'}, inplace=True)

    # number_of_schools_mcoc_sorted = number_of_schools_mcoc.sort_values(by='school_count', ascending=False)

    # number_of_schools_mcoc_colors = ['#04508c', '#037DEE', '#369EFF', '#930F22', '#E11C38', '#FF899A']

    # number_of_schools_mcoc_chart = px.pie(
    #     number_of_schools_mcoc_sorted,
    #     names='mod_coc',
    #     values='school_count',
    #     hole=0.45,
    #     # title='<b>Number of Schools by Program Offerings</b>',
    #     color_discrete_sequence=number_of_schools_mcoc_colors
    # )

    # number_of_schools_mcoc_chart.update_traces(
    #     textposition='inside',
    #     textinfo='label+value',
    #     textfont=dict(size=14, color='white'),
    #     hovertemplate='<b>%{label}</b><br>Schools: %{value:,}<extra></extra>'
    # )

    # number_of_schools_mcoc_chart.update_layout(
    #     autosize=True,
    #     showlegend=True,
    #     title_font_size=18,
    #     title_font_color='#3C6382',
    #     title_x=0.5,
    #     margin=dict(l=0, r=0, t=0, b=0),
    #     plot_bgcolor='#FFFFFF',
    #     font=dict(family='Inter, sans-serif', color='#3C6382'),
    #     legend=dict(
    #         orientation='h',
    #         yanchor='bottom',
    #         y=-0.5,
    #         xanchor='center',
    #         x=0.5,
    #         title=None,
    #         font=dict(size=14),
    #     )
    # )


    # number_of_schools_mcoc_chart
    
    return dcc.Graph(figure=number_of_schools_mcoc_chart, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #################################################################################



# #################################################################################
# ##  --- CHART: Gender Distribution Aross MCOC types
# #################################################################################

@callback(
    Output('offering_gender-distribution', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    gender_distribution_mcoc = FILTERED_DATA.groupby(['mod_coc', 'gender'])['counts'].sum().reset_index()

    gender_distribution_mcoc['gender'] = gender_distribution_mcoc['gender'].str.title().replace({'M': 'Male', 'F': 'Female'})

    gender_distribution_chart = px.bar(
        gender_distribution_mcoc,
        x='mod_coc',
        y='counts',
        color='gender',
        barmode='group',
        # title='<b>Gender Distribution Across Program Offerings</b>',
        color_discrete_map={
            'Male': '#5DB7FF',     
            'Female': '#FF5B72'    
        },
        labels={
            'mod_coc': 'Program Offering',
            'counts': 'Total Students',
            'gender': 'Gender'
        }
    )

    gender_distribution_chart.update_layout(
        autosize=True,
        # xaxis_title='Program Offering',
        # yaxis_title='Number of Students',
        title_font_size=18,
        title_font_color='#3C6382',
        title_x=0.5,
        plot_bgcolor='rgba(255, 255, 255, 0.5)',
        font=dict(family='Inter, sans-serif', color='#3C6382'),
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        xaxis=dict(
            title=None,
            tickangle=-45,
            tickfont=dict(size=11),
            showline=True,
            linecolor="#3C6382",
            linewidth=1
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=11),
            showline=True,
            linecolor="#3C6382",
            linewidth=1
        ),
        legend=dict(
            title='Gender',
            font=dict(size=10),
            orientation='h',      # horizontal layout
            yanchor='bottom',
            y=1.02,               # slightly above the plot
            xanchor='center',
            x=0.5,                # centered horizontally
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
        )
    )

    gender_distribution_chart.update_yaxes(tickformat='.0s')

    gender_distribution_chart
    
    return dcc.Graph(figure=gender_distribution_chart, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #################################################################################



# #################################################################################
# ##  --- CHART: MCOC Types Ranked by Total Student Enrollment
# #################################################################################

@callback(
    Output('offering_ranked-mcoc', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    State('is-all-year', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data, mode):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    if mode:
        mcoc_enrollment = FILTERED_DATA.groupby(['year', 'mod_coc'])['counts'].sum().reset_index().groupby('mod_coc', as_index=False)['counts'].mean()

    else:
        mcoc_enrollment = FILTERED_DATA.groupby('mod_coc')['counts'].sum().reset_index()

    
    mcoc_enrollment_sorted = mcoc_enrollment.sort_values(by='counts', ascending=False)

    ranked_mcoc_chart = px.bar(
        mcoc_enrollment_sorted,
        x='counts',
        y='mod_coc',
        orientation='h',
        # title='<b>MCOC Types Ranked by Total Student Enrollment</b>',
        labels={
            'mod_coc': 'MCOC Type',
            'counts': 'Total Students'
        },
        hover_data={'mod_coc': False, 'counts': True}
    )

    ranked_mcoc_chart.update_traces(
        marker_color='#5DB7FF',
        showlegend=False,
    )

    ranked_mcoc_chart.update_layout(
        showlegend=False,
        autosize=True,
        title={
            # 'text': '<b>MCOC Types Ranked by Total Student Enrollment</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Inter, sans-serif', 'color': '#3C6382'}
        },
        # xaxis_title='Number of Students',
        # yaxis_title='Programs',
        font=dict(family='Inter, sans-serif', size=14, color='#3C6382'), 
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        yaxis=dict(
            categoryorder='total ascending',
            title=None,
            tickfont=dict(size=11),
            ticksuffix="  "
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False,
            tickformat='.0s',
            title=None,
            tickfont=dict(size=11),
        ),
        plot_bgcolor='#FFFFFF' 
    )

    ranked_mcoc_chart
    
    return dcc.Graph(figure=ranked_mcoc_chart, config={"responsive": True}, style={"width": "100%", "height": "100%"})


# #################################################################################



# #################################################################################
# ##  --- CHART: Geographic Distribution of Program Offerings
# #################################################################################

# @callback(
#     Output('', 'children'),
#     Input('chart-trigger', 'data'),
#     State('filtered_values', 'data'),
    # prevent_initial_call=True
# )

# def update_graph(trigger, data):
#     FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
#     return dcc.Graph(figure=)




# #################################################################################



# #################################################################################
# ##  --- CHART: Enrollment Distribution by Grade Level
# #################################################################################

@callback(
    Output('offering_enroll_dist', 'children'),
    Output('offering-highest-grade', 'children'),
    Output('offering-highest-count', 'children'),
    Output('offering-lowest-grade', 'children'),
    Output('offering-lowest-count', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    State('is-all-year', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data, mode):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    order = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'ES NG', 'G7', 'G8', 'G9', 'G10', 'JHS NG', 'G11', 'G12']

    FILTERED_DATA['school-level'] = FILTERED_DATA['grade'].apply(
        lambda x: 'JHS' if x in ['G7', 'G8', 'G9', 'G10', 'JHS NG'] else (
            'SHS' if x in ['G11', 'G12'] else 'ELEM')
    )
    
    if mode:
        # Group by year and school-level, grade, then average over years
        query = (
            FILTERED_DATA.groupby(['year', 'school-level', 'grade'], as_index=False)['counts'].sum()
            .groupby(['school-level', 'grade'], as_index=False)['counts'].mean()
        )
    else:
        # Just group directly by school-level and grade
        query = (
            FILTERED_DATA.groupby(['school-level', 'grade'], as_index=False)['counts'].sum()
        )

    query = query[query['counts'] != 0]
    query['grade'] = pd.Categorical(query['grade'], categories=order, ordered=True)
    query = query.sort_values('grade')
    query['formatted_counts'] = query['counts'].apply(smart_truncate_number)
    
    grade_name_map = {
        'K': 'Kindergarten',
        'G1': 'Grade 1',
        'G2': 'Grade 2',
        'G3': 'Grade 3',
        'G4': 'Grade 4',
        'G5': 'Grade 5',
        'G6': 'Grade 6',
        'ES NG': 'ES NG',
        'G7': 'Grade 7',
        'G8': 'Grade 8',
        'G9': 'Grade 9',
        'G10': 'Grade 10',
        'JHS NG': 'JHS NG',
        'G11': 'Grade 11',
        'G12': 'Grade 12',
    }

    query['renamed-grade'] = query['grade'].map(grade_name_map)
    
    # Get extremes
    highest = query.loc[query['counts'].idxmax()]
    lowest = query.loc[query['counts'].idxmin()]
    
    highest_grade = highest["renamed-grade"]
    highest_count = highest["counts"]
    lowest_grade = lowest["renamed-grade"]
    lowest_count = lowest["counts"]

    # print(query['formatted_counts'])
    # print(query.head())

    offering_enroll_dist = px.bar(
        query, 
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

    offering_enroll_dist.update_traces(
        textposition='outside',
        cliponaxis=False,
        textfont=dict(size=8, color="#04508c"),
        hovertemplate='Education Level: %{customdata[0]}<br>Enrollees: %{x}<br>Grade-level: %{y}',
    )

    offering_enroll_dist.update_layout(
        autosize=True,
        margin={"l": 8, "r": 8, "t": 8, "b": 8},
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        yaxis=dict(
            automargin=True,
            title=None,
            tickfont=dict(size=9, color="#9DADBD"),
            ticksuffix="  "
        ),
        xaxis=dict(
            automargin=True,
            title=None,
            visible=False,
            categoryorder='array',
            categoryarray=order
        ),
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.025,
            xanchor="center",
            x=0.45
        )
    )

    return (dcc.Graph(figure=offering_enroll_dist, config={"responsive": True}, style={"width": "100%", "height": "100%"}), highest_grade, f"{highest_count:,}", lowest_grade, f"{lowest_count:,}")

    # grade_enrollment = FILTERED_DATA.groupby('grade')['counts'].sum().reset_index()
    # grade_enrollment

    # offering_enroll_dist = px.bar(
    #     grade_enrollment,
    #     x='grade',
    #     y='counts',
    #     # title='<b>Enrollment Distribution by Grade Level</b>',
    #     labels={'grade': 'Grade Level', 'counts': 'Number of Enrollees'},
    #     text='counts'
    # )

    # offering_enroll_dist.update_traces(
    #     textposition='outside',
    #     marker_color='#EA6074' 
    # )

    # offering_enroll_dist.update_layout(
    #     xaxis_title='Grade Level',
    #     yaxis_title='Number of Enrollees',
    #     uniformtext_minsize=8,
    #     uniformtext_mode='hide'
    # )
    
    # offering_enroll_dist
    
    # return dcc.Graph(figure=offering_enroll_dist, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #################################################################################
# ##  --- CHART: Number of MCOC Offerings per Location by School Level
# #################################################################################

@callback(
    Output('offering_mcoc-offerings-per-loc', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    FILTERED_DATA['school_level'] = FILTERED_DATA['grade'].apply(
        lambda x: 'ELEM' if x in ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6'] else 
                ('JHS' if x in ['G7', 'G8', 'G9', 'G10'] else 'SHS')
    )

    FILTERED_DATA['grade'] = FILTERED_DATA['grade'].astype(str).str.upper().str.strip()

    region_schools_df = FILTERED_DATA[FILTERED_DATA['school_level'] != 'UNKNOWN']

    region_grouped_schools = region_schools_df.groupby(['region', 'school_level'])['beis_id'].nunique().reset_index()

    region_stacked_chart = px.bar(
        region_grouped_schools,
        x='region',
        y='beis_id',
        color='school_level',
        barmode='stack',
        # title='<b>Number of Schools per Region by School Level</b>',
        color_discrete_map={
            'ELEM': '#930F22',
            'JHS': '#E11C38',
            'SHS': '#FF899A',
        },
        labels={
            'region': 'Region',
            'beis_id': 'Number of Schools',
            'school_level': 'School Level'
        }
    )

    region_stacked_chart.update_layout(
        autosize=True,
        title={
            # 'text': '<b>Number of Schools per Region by School Level</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Inter, sans-serif', 'color': '#3C6382'}
        },
        font={'family': 'Inter, sans-serif', 'size': 12, 'color': '#3C6382'},
        # xaxis_title='Region',
        # yaxis_title='Total Number of Schools',
        legend_title='School Level',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            tickangle=-45,
            showgrid=True,
            # gridcolor='rgba(0,0,0,0.05)',
            title=None,
            showline=True,
            linecolor="#3C6382",
            linewidth=1,
            tickfont=dict(size=11),
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='center',
            x=0.5,
            title=None,
            font=dict(size=13),
        ),
        plot_bgcolor='#FFFFFF',
        yaxis=dict(
            title=None,
            type='log',  # Set y-axis to logarithmic scale
            tickvals=[10, 100, 1000, 10000, 50000],  # Custom tick values
            ticktext=["10", "100", "1K", "10K", "50K"],  # Custom tick labels
            showline=True,
            linecolor="#3C6382",
            linewidth=1,
            tickfont=dict(size=11),
        ),
    )

    region_stacked_chart.update_traces(
        # marker_line_color='#FFFFFF',
        marker_line_width=0
    )

    return dcc.Graph(figure=region_stacked_chart, config={"responsive": True}, style={"width": "100%", "height": "100%"})


# #################################################################################



# #################################################################################
# ##  --- INDICATOR: Locations with the Highest and Lowest Number of Offerings
# #################################################################################
@callback(
    Output('offering_location-extremes', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
)
def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data, enrollment_db_engine)

    FILTERED_DATA['school_level'] = FILTERED_DATA['grade'].apply(
        lambda x: 'ELEM' if x in ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6']
        else ('JHS' if x in ['G7', 'G8', 'G9', 'G10']
        else ('SHS' if x in ['G11', 'G12'] else 'UNKNOWN'))
    )

    FILTERED_DATA = FILTERED_DATA[FILTERED_DATA['school_level'] != 'UNKNOWN']

    grouped = FILTERED_DATA.groupby(['school_level', 'region'])['counts'].sum().reset_index()
    highest = grouped.loc[grouped.groupby('school_level')['counts'].idxmax()].reset_index(drop=True)
    lowest = grouped.loc[grouped.groupby('school_level')['counts'].idxmin()].reset_index(drop=True)

    high_low_combined = pd.concat([ 
        highest.assign(rank='Highest'),
        lowest.assign(rank='Lowest')
    ], ignore_index=True)

    indicator_chart = go.Figure()

    # Section headers
    indicator_chart.add_annotation(
        text="<b>HIGHEST</b>",
        x=0.5, y=1, showarrow=False,
        font={'size': 16, 'family': 'Inter, sans-serif', 'color': '#1B4F72'},
        xref="paper", yref="paper"
    )
    indicator_chart.add_annotation(
        text="<b>LOWEST</b>",
        x=0.5, y=0.47, showarrow=False,
        font={'size': 16, 'family': 'Inter, sans-serif', 'color': '#1B4F72'},
        xref="paper", yref="paper"
    )

    # Add indicators
    for _, row in high_low_combined.iterrows():
        row_position = 0 if row['rank'] == 'Highest' else 1
        column_position = {'ELEM': 0, 'JHS': 1, 'SHS': 2}.get(row['school_level'], 2)

        icon = '🏫' if row['school_level'] == 'ELEM' else ('📚' if row['school_level'] == 'JHS' else '🎓')
        region_text = f"<span style='font-size:12px; color:#7B8788'>{row['region']}</span>"
        title_text = f"<b>{icon} {row['school_level']}</b><br>{region_text}"

        indicator_chart.add_trace(go.Indicator(
            mode='number',
            value=row['counts'],
            title={'text': title_text},
            number={ 
                'valueformat': '.2s',
                'font': {'size': 42, 'color': '#1B4F72'}
            },
            domain={'row': row_position, 'column': column_position}
        ))

    indicator_chart.update_layout(
        grid={'rows': 2, 'columns': 3, 'pattern': "independent"},
        template="plotly_white",
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        title={
            # 'text': "<b>Regions with Highest and Lowest Offerings <br>per School Level</b>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Inter, sans-serif', 'color': '#1B4F72'}
        },
        plot_bgcolor="#FFFFFF",
        font={'family': 'Inter, sans-serif', 'size': 13, 'color': '#3C6382'}
    )

    return dcc.Graph(figure=indicator_chart, config={"responsive": True}, style={"width": "100%", "height": "100%"})


# #################################################################################



# #################################################################################
# ##  --- INDICATOR: Total Number of Enrollees Across All MCOC Types
# #################################################################################

@callback(
    Output('offering_enrollees_num', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    grouped_by_MCOC= FILTERED_DATA.groupby('mod_coc', as_index=False)['counts'].sum()
    grouped_by_MCOC

    total_All_Offering = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "All Offering", 'counts'].values[0]
    total_All_Offering = (total_All_Offering)

    total_ES_JHS = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "ES and JHS", 'counts'].values[0]
    total_ES_JHS = (total_ES_JHS)

    total_JHS_SHS = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "JHS with SHS", 'counts'].values[0]
    total_JHS_SHS = (total_JHS_SHS)

    total_Pure_ES = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "Purely ES", 'counts'].values[0]
    total_Pure_ES = (total_Pure_ES)

    total_Pure_JHS = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "Purely JHS", 'counts'].values[0]
    total_Pure_JHS = (total_Pure_JHS)

    total_Pure_SHS = grouped_by_MCOC.loc[grouped_by_MCOC["mod_coc"] == "Purely SHS", 'counts'].values[0]
    total_Pure_SHS = (total_Pure_SHS)

    mod_coc_categories = ["All Offering", "ES and JHS", "JHS with SHS", "Purely ES", "Purely JHS", "Purely SHS"]
    counts = [total_All_Offering, total_ES_JHS, total_JHS_SHS, total_Pure_ES, total_Pure_JHS, total_Pure_SHS]

    header_color = '#74B8F6'       
    cell_color = '#D6E9FA'        

    table_fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Modified COC (Offering)</b>", "<b>Total</b>"],
            fill_color=header_color,
            font=dict(color='white', size=14),
            align='left'
        ),
        cells=dict(
            values=[mod_coc_categories, counts],
            fill_color=cell_color,
            font=dict(color='black', size=12),
            align='left'
        )
    )])

    # table_fig.update_layout(title_text="Total Number of Enrollees Across All MCOC Types")

    table_fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),  # Remove margins
        height=None,  # Let container control the height
    )
    
    return dcc.Graph(figure=table_fig, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #################################################################################

@callback(
    Output('offering_newschools_chart', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # Count the number of *new* unique schools per year per program type
    new_schools = FILTERED_DATA.drop_duplicates(subset=['beis_id', 'mod_coc']).groupby(['year', 'mod_coc']).size().reset_index(name='num_new_schools')

    # Create a visually appealing line chart
    newschools_chart = px.line(
        new_schools,
        x='year',
        y='num_new_schools',
        color='mod_coc',
        markers=True,
        line_shape='spline',  # Smooth curves
        labels={
            'year': 'Year',
            'num_new_schools': 'Number of New Schools',
            'mod_coc': 'Program Type'
        },
        color_discrete_sequence=px.colors.qualitative.Safe  # Soft, colorblind-friendly palette
    )

    # Layout enhancements
    newschools_chart.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Inter, sans-serif", size=12, color="#3C6382"),
        legend=dict(
            title=None,
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5,
            font=dict(size=12)
        ),
        xaxis=dict(
            title=None,
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickfont=dict(size=11),
            linecolor='#3C6382',
            linewidth=1,
            type="category"
        ),
        yaxis=dict(
            title=None,
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            tickfont=dict(size=11),
            linecolor='#3C6382',
            linewidth=1
        ),
        plot_bgcolor='#FFFFFF',
    )

    # Trace enhancements
    newschools_chart.update_traces(
        mode='lines+markers',
        line=dict(width=3),
        marker=dict(size=8, symbol='circle', line=dict(width=1, color='white')),
        textposition='top center'
    )

    newschools_chart
    
    return dcc.Graph(figure=newschools_chart, config={"responsive": True}, style={"width": "100%", "height": "100%"})

# #########################################################################################

@callback(
    Output('school_level_area_chart', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # Ensure school-level column is already created
    FILTERED_DATA['school-level'] = FILTERED_DATA['grade'].apply(
        lambda x: 'JHS' if x in ['G7', 'G8', 'G9', 'G10', 'JHS NG'] else (
            'SHS' if x in ['G11', 'G12'] else 'ES')
    )

    # Convert year to numeric (in case it's not already)
    FILTERED_DATA['year'] = pd.to_numeric(FILTERED_DATA['year'], errors='coerce').astype(int)

    # Group by year and school-level, then sum the counts
    grouped_school_level = FILTERED_DATA.groupby(['year', 'school-level'], as_index=False)['counts'].sum()

    # Create the area chart
    school_level_area_chart = px.area(
        grouped_school_level,
        x='year',
        y='counts',
        color='school-level',
        line_group='school-level',
        markers=True,
        color_discrete_map={
            'ES': '#930F22',   # Elementary
            'JHS': '#E11C38',  # Junior High School
            'SHS': '#FF899A'   # Senior High School
        },
        labels={
            'year': 'Year',
            'counts': 'Number of Students',
            'school-level': 'School Level'
        }
    )

    # Update layout for visual appeal
    school_level_area_chart.update_traces(
        mode='lines+markers',
        marker=dict(size=8),
        line=dict(width=3),
        hovertemplate='<b>Year</b>: %{x}<br><b>Count</b>: %{y}<br><b>Level</b>: %{legendgroup}<extra></extra>'
    )

    school_level_area_chart.update_layout(
        template='plotly_white',
        autosize=True,
        font=dict(color='#3C6382', family='Inter, sans-serif'),
        legend=dict(
            title='School Level',
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5,
            font=dict(size=12)
        ),
        xaxis=dict(
            title=None,
            tickfont=dict(size=11),
            linecolor="#3C6382",
            linewidth=1,
            type="category"
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=11),
            linecolor="#3C6382",
            linewidth=1
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    # To display in Dash
    return dcc.Graph(figure=school_level_area_chart, config={"responsive": True}, style={"width": "100%", "height": "100%"})


# #########################################################################################
# # ----------------------------------------------------------
# shs_df = auto_extract(['strand', 'track', 'shs_grade', 'counts'], is_specific=False)
# shs_df