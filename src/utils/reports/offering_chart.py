import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State, Patch

# important part
from src.data import enrollment_db_engine, smart_filter

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

    number_of_schools_mcoc = FILTERED_DATA.groupby('mod_coc')['beis_id'].nunique().reset_index()
    number_of_schools_mcoc.rename(columns={'beis_id': 'school_count'}, inplace=True)

    number_of_schools_mcoc_sorted = number_of_schools_mcoc.sort_values(by='school_count', ascending=False)

    number_of_schools_mcoc_colors = ['#04508c', '#037DEE', '#369EFF', '#930F22', '#E11C38', '#FF899A']

    number_of_schools_mcoc_chart = px.pie(
        number_of_schools_mcoc_sorted,
        names='mod_coc',
        values='school_count',
        hole=0.45,
        title='<b>Number of Schools by Program Offerings</b>',
        color_discrete_sequence=number_of_schools_mcoc_colors
    )

    number_of_schools_mcoc_chart.update_traces(
        textposition='inside',
        textinfo='label+value',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>Schools: %{value:,}<extra></extra>'
    )

    number_of_schools_mcoc_chart.update_layout(
        autosize=True,
        showlegend=True,
        title_font_size=18,
        title_font_color='#3C6382',
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20),
        height=450,
        plot_bgcolor='#FFFFFF',
        font=dict(family='Inter, sans-serif', color='#3C6382'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='center',
            x=0.5,
            title=None,
            font=dict(size=14),
        )
    )


    number_of_schools_mcoc_chart
    
    return dcc.Graph(figure=number_of_schools_mcoc_chart)

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
        title='<b>Gender Distribution Across Program Offerings</b>',
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
        xaxis_title='Program Offering',
        yaxis_title='Number of Students',
        title_font_size=18,
        title_font_color='#3C6382',
        title_x=0.5,
        plot_bgcolor='rgba(255, 255, 255, 0.5)',
        font=dict(family='Inter, sans-serif', color='#3C6382'),
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
        legend=dict(
            title='Gender',
            font=dict(size=14),
            x=1.05,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)',   
            bordercolor='rgba(0,0,0,0)', 
        )
    )

    gender_distribution_chart.update_yaxes(tickformat='.0s')

    gender_distribution_chart
    
    return dcc.Graph(figure=gender_distribution_chart)

# #################################################################################



# #################################################################################
# ##  --- CHART: MCOC Types Ranked by Total Student Enrollment
# #################################################################################

@callback(
    Output('offering_ranked-mcoc', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    mcoc_enrollment = FILTERED_DATA.groupby('mod_coc')['counts'].sum().reset_index()

    mcoc_enrollment_sorted = mcoc_enrollment.sort_values(by='counts', ascending=False)

    ranked_mcoc_chart = px.bar(
        mcoc_enrollment_sorted,
        x='counts',
        y='mod_coc',
        orientation='h',
        title='<b>MCOC Types Ranked by Total Student Enrollment</b>',
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
            'text': '<b>MCOC Types Ranked by Total Student Enrollment</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Inter, sans-serif', 'color': '#3C6382'}
        },
        xaxis_title='Number of Students',
        yaxis_title='Programs',
        font=dict(family='Inter, sans-serif', size=14, color='#3C6382'), 
        margin={"l": 40, "r": 40, "t": 60, "b": 40},
        height=500,
        yaxis={'categoryorder': 'total ascending'},
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False,
            tickformat='.0s'
        ),
        plot_bgcolor='#FFFFFF' 
    )

    ranked_mcoc_chart
    
    return dcc.Graph(figure=ranked_mcoc_chart)


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
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    # prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    grade_enrollment = FILTERED_DATA.groupby('grade')['counts'].sum().reset_index()
    grade_enrollment

    offering_enroll_dist = px.bar(
        grade_enrollment,
        x='grade',
        y='counts',
        title='<b>Enrollment Distribution by Grade Level</b>',
        labels={'grade': 'Grade Level', 'counts': 'Number of Enrollees'},
        text='counts'
    )

    offering_enroll_dist.update_traces(
        textposition='outside',
        marker_color='#EA6074' 
    )

    offering_enroll_dist.update_layout(
        xaxis_title='Grade Level',
        yaxis_title='Number of Enrollees',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    
    offering_enroll_dist
    
    return dcc.Graph(figure=offering_enroll_dist)

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
        title='<b>Number of Schools per Region by School Level</b>',
        color_discrete_map={
            'ELEM': '#FF899A',
            'JHS': '#E11C38',
            'SHS': '#930F22'
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
            'text': '<b>Number of Schools per Region by School Level</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Inter, sans-serif', 'color': '#3C6382'}
        },
        font={'family': 'Inter, sans-serif', 'size': 12, 'color': '#3C6382'},
        xaxis_title='Region',
        yaxis_title='Total Number of Schools',
        legend_title='School Level',
        margin=dict(l= 10, r=10, t=60, b=10),
        height=550,
        xaxis=dict(
            tickangle=45,
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='center',
            x=0.4,
            title=None,
            font=dict(size=14),
        ),
        plot_bgcolor='#FFFFFF'
    )

    region_stacked_chart.update_traces(
        marker_line_color='#FFFFFF',
        marker_line_width=2
    )

    region_stacked_chart
    
    return dcc.Graph(figure=region_stacked_chart)





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
        x=0.5, y=1.10, showarrow=False,
        font={'size': 16, 'family': 'Inter, sans-serif', 'color': '#3C6382'},
        xref="paper", yref="paper"
    )
    indicator_chart.add_annotation(
        text="<b>LOWEST</b>",
        x=0.5, y=0.47, showarrow=False,
        font={'size': 16, 'family': 'Inter, sans-serif', 'color': '#3C6382'},
        xref="paper", yref="paper"
    )

    # Add indicators
    for _, row in high_low_combined.iterrows():
        row_position = 0 if row['rank'] == 'Highest' else 1
        column_position = {'ELEM': 0, 'JHS': 1, 'SHS': 2}.get(row['school_level'], 2)

        title_text = f"<b>{row['school_level']}</b><br><span style='font-size:13px; font-style:italic'>{row['region']}</span>"

        indicator_chart.add_trace(go.Indicator(
            mode='number',
            value=row['counts'],
            title={'text': title_text},
            number={
                'valueformat': '.2s',
                'font': {'size': 44, 'color': '#3C6382'}
            },
            domain={'row': row_position, 'column': column_position}
        ))

    indicator_chart.update_layout(
        grid={'rows': 2, 'columns': 3, 'pattern': "independent"},
        template="plotly_white",
        height=500,
        margin={"l": 40, "r": 40, "t": 140, "b": 60},
        title={
            'text': "<b>Regions with Highest and Lowest Offerings per School Level</b>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'family': 'Inter, sans-serif', 'color': '#3C6382'}
        },
        plot_bgcolor="#FFFFFF",
        font={'family': 'Inter, sans-serif', 'size': 13, 'color': '#3C6382'}
    )

    return dcc.Graph(figure=indicator_chart)

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

    table_fig.update_layout(title_text="Total Number of Enrollees Across All MCOC Types")

    table_fig
    
    return dcc.Graph(figure=table_fig)

# #################################################################################