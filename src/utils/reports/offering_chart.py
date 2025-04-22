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
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # 2. Group by 'mod_coc' (program offering type) and sum the total number of students
    number_of_schools_mcoc = FILTERED_DATA.groupby('mod_coc')['counts'].sum().reset_index()

    # 3. Sort the data by total number of students in descending order
    number_of_schools_mcoc_sorted = number_of_schools_mcoc.sort_values(by='counts', ascending=False)

    # 4. Define the custom color palette for the chart
    number_of_schools_mcoc_colors = ['#04508c', '#037DEE', '#369EFF', '#930F22', '#E11C38', '#FF899A']

    # 5. Create the pie chart (donut chart) using Plotly Express
    number_of_schools_mcoc_chart = px.pie(
        number_of_schools_mcoc_sorted,
        names='mod_coc',
        values='counts',
        hole=0.45,
        title='Number of Schools by Program Offerings',
        color_discrete_sequence=number_of_schools_mcoc_colors
    )

    # 6. Update the chart appearance and interactivity
    number_of_schools_mcoc_chart.update_traces(
        textposition='inside',
        textinfo='label+value',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>Total: %{value:,} students<extra></extra>'
    )
    
    return dcc.Graph(figure=number_of_schools_mcoc_chart)

# #################################################################################



# #################################################################################
# ##  --- CHART: Gender Distribution Aross MCOC types
# #################################################################################

@callback(
    Output('offering_gender-distribution', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # 2. Group by mod_coc and gender, then sum student counts
    gender_distribution_mcoc = FILTERED_DATA.groupby(['mod_coc', 'gender'])['counts'].sum().reset_index()

    # 3. Standardize gender labels
    gender_distribution_mcoc['gender'] = gender_distribution_mcoc['gender'].str.title().replace({'M': 'Male', 'F': 'Female'})

    # 4. Bar chart setup
    gender_distribution_chart = px.bar(
        gender_distribution_mcoc,
        x='mod_coc',
        y='counts',
        color='gender',
        barmode='group',
        title='Gender Distribution Across Program Offerings',
        color_discrete_map={
            'Male': '#04508c',     # Primary color
            'Female': '#E11C38'    # Secondary color
        },
        labels={
            'mod_coc': 'Program Offering',
            'counts': 'Total Students',
            'gender': 'Gender'
        }
    )

    # 5. Update layout to match your pie chart style
    gender_distribution_chart.update_layout(
        xaxis_title='Program Offering',
        yaxis_title='Number of Students',
        title_font_size=18,
        title_font_color='#3C6382',
        title_x=0.5,
        paper_bgcolor='#F0F0F0',
        plot_bgcolor='rgba(255, 255, 255, 0.5)',
        font=dict(family='Inter, sans-serif', color='#3C6382'),
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
        legend=dict(
            title='Gender',
            font=dict(size=14),
            x=1,
            y=1,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)',   # Transparent background
            bordercolor='rgba(0,0,0,0)',  # No border
        )
    )
    
    # 6. Optional: format y-axis ticks with commas
    gender_distribution_chart.update_yaxes(tickformat=',')

    # 7. Display the chart
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
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)
    
    # 2. Group data by mod_coc and sum student counts
    mcoc_enrollment = FILTERED_DATA.groupby('mod_coc')['counts'].sum().reset_index()

    # 3. Sort by counts in descending order
    mcoc_enrollment_sorted = mcoc_enrollment.sort_values(by='counts', ascending=False)

    # 4. Create a ranked horizontal bar chart with custom blue shades 
    custom_blues = ['#A8E8FF', '#5DB7FF', '#369EFF', '#037DEE', '#04508c']

    ranked_mcoc_chart = px.bar(
        mcoc_enrollment_sorted,
        x='counts',
        y='mod_coc',
        orientation='h',
        title='MCOC Types Ranked by Total Student Enrollment',
        color='counts',
        color_continuous_scale=custom_blues,  # Custom blue gradient, no white
        labels={
            'mod_coc': 'MCOC Type',
            'counts': 'Total Students'
        },
        hover_data={'mod_coc': False, 'counts': True}
    )

    # 5. Add a border around the bars using a subtle darker blue
    ranked_mcoc_chart.update_traces(
        marker_line_color='#3C6382',
        marker_line_width=1
    )
    # 6. Layout and design adjustments for uniform styling
    ranked_mcoc_chart.update_layout(
        title={
            'text': 'MCOC Types Ranked by Total Student Enrollment',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 26, 'family': 'Inter, sans-serif', 'color': '#3C6382'}
        },
        xaxis_title='Number of Students',
        yaxis_title='Programs',
        font=dict(family='Inter, sans-serif', color='#3C6382'),
        margin={"l": 40, "r": 40, "t": 60, "b": 40},
        height=500,
        yaxis={'categoryorder': 'total ascending'},
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False,
            tickformat=','
        ),
        paper_bgcolor='#F0F0F0',
        plot_bgcolor='#FFFFFF'  # Pure white plot area to contrast with bar color
    )


    # 7. Display the final chart
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
#     prevent_initial_call=True
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
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    grade_enrollment = FILTERED_DATA.groupby('grade')['counts'].sum().reset_index()
    grade_enrollment

    offering_enroll_dist = px.bar(
        grade_enrollment,
        x='grade',
        y='counts',
        title='Enrollment Distribution by Grade Level',
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
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

    # 2. Create a new column for school level based on grade
    FILTERED_DATA['school_level'] = FILTERED_DATA['grade'].apply(
        lambda x: 'ELEM' if x in ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6'] else 
                ('JHS' if x in ['G7', 'G8', 'G9', 'G10'] else 'SHS')
    )

    # 3. Group data by region and school level, then sum the number of offerings
    region_grouped = FILTERED_DATA.groupby(['region', 'school_level'])['counts'].sum().reset_index()

    # 4. Create a stacked bar chart
    region_stacked_chart = px.bar(
        region_grouped,
        x='region',
        y='counts',
        color='school_level',
        barmode='stack',
        title='Total Number of Offerings per Region by School Level',
        color_discrete_map={
            'ELEM': '#FF899A',
            'JHS': '#E11C38',
            'SHS': '#930F22'
        },
        labels={
            'region': 'Region',
            'counts': 'Number of Offerings',
            'school_level': 'School Level'
        }
    )
    
    # 5. Update chart layout and appearance
    region_stacked_chart.update_layout(
        title={
            'text': 'Total Number of Offerings per Region by School Level',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'family': 'Inter, sans-serif', 'color': '#3C6382'}
        },
        font={'family': 'Inter, sans-serif', 'size': 14, 'color': '#3C6382'},
        xaxis_title='Region',
        yaxis_title='Total Number of Offerings',
        legend_title='School Level',
        margin={"l": 40, "r": 40, "t": 60, "b": 100},
        height=550,
        xaxis_tickangle=45,
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)'
        ),
        legend=dict(
            x=1,
            y=1,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0)'
        ),
        paper_bgcolor='#F0F0F0',
        plot_bgcolor='#FFFFFF'
    )

    # 6. Add white borders between stacked segments for clarity
    region_stacked_chart.update_traces(
        marker_line_color='#FFFFFF',
        marker_line_width=2
    )

    # 7. Display the final chart
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
    prevent_initial_call=True
)

def update_graph(trigger, data):
    FILTERED_DATA = smart_filter(data ,enrollment_db_engine)

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
    ])

    indicator_chart = go.Figure()

    for _, row in high_low_combined.iterrows():
        indicator_chart.add_trace(go.Indicator(
            mode='number',
            value=row['counts'],
            title={
                'text': f"<b>{row['school_level']}</b><br><span style='font-size:13px'>{row['rank']} in {row['region']}</span>"
            },
            number={
                'valueformat': ',',
                'font': {'color': '#3C6382'}
            },
            domain={
                'row': 0 if row['rank'] == 'Highest' else 1,
                'column': 0 if row['school_level'] == 'ELEM' else (1 if row['school_level'] == 'JHS' else 2)
            }
        ))

    indicator_chart.update_layout(
        grid={'rows': 2, 'columns': 3, 'pattern': "independent"},
        template="plotly_white",
        height=600,
        title={
            'text': "Regions with Highest and Lowest Offerings per School Level",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'family': 'Inter, sans-serif'}
        },
        margin={"l": 50, "r": 50, "t": 80, "b": 50}
    )

    indicator_chart
    
    return dcc.Graph(figure=indicator_chart)




# #################################################################################



# #################################################################################
# ##  --- INDICATOR: Total Number of Enrollees Across All MCOC Types
# #################################################################################

@callback(
    Output('offering_enrollees_num', 'children'),
    Input('chart-trigger', 'data'),
    State('filtered_values', 'data'),
    prevent_initial_call=True
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