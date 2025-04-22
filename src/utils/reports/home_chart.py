import os, sys
import time
import numpy as np
import pandas as pd
import dash
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, State, Patch


# important part
from src.data import enrollment_db_engine, smart_filter


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from utils.get_data import auto_extract


# ----------------------------------------------------------
from src.utils.extras_utils import smart_truncate_number



#################################################################################
##                     MAIN DATAFRAME BASED FROM THE QUERY                     ##
#################################################################################

# -- Create the appropriate plot

@callback(
    Output('home-enrollment-per-region', 'figure'),
    Input("url", "pathname")
)
def update_graph(pathname):
    if pathname != "/":
        return dash.no_update

    
    BASE_DF = smart_filter({}, _engine=enrollment_db_engine)
    BASE_DF[['grade', 'counts']]

    order = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'ES NG', 'G7', 'G8', 'G9', 'G10', 'JHS NG', 'G11', 'G12']

    BASE_DF['school-level'] = BASE_DF['grade'].apply(
        lambda x: 'JHS' if x in ['G7', 'G8', 'G9', 'G10', 'JHS NG'] else (
            'SHS' if x in ['G11', 'G12'] else 'ELEM')
    )

    query = BASE_DF.groupby(['school-level','grade'], as_index=False)[['counts']].sum()
    query['grade'] = pd.Categorical(query['grade'], categories=order, ordered=True)
    query = query.sort_values('grade')
    query['formatted_counts'] = query['counts'].apply(smart_truncate_number)

    fig = px.bar(
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

    fig.update_traces(
        textposition='outside',
        cliponaxis=False,
        textfont=dict(size=8, color="#04508c"),
        hovertemplate='Education Level: %{customdata[0]}<br>Enrollees: %{x}<br>Grade-level: %{y}',
    )

    fig.update_layout(
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

    patched_fig = Patch()
    patched_fig["data"] = fig.data
    patched_fig["layout"] = fig.layout

    return patched_fig


# #########################################################################################
# # ----------------------------------------------------------
# shs_df = auto_extract(['strand', 'track', 'shs_grade', 'counts'], is_specific=False)
# shs_df

# es_count = BASE_DF[BASE_DF['school-level'] == 'ELEM']['counts'].sum()
# jhs_count = BASE_DF[BASE_DF['school-level'] == 'JHS']['counts'].sum()
# shs_count = BASE_DF[BASE_DF['school-level'] == 'SHS']['counts'].sum()

# total_enrollees = es_count + jhs_count + shs_count
# total_enrollees

# total_enrollees_formatted = smart_truncate_number(total_enrollees)
# total_enrollees_formatted

# ## -- INDICATORS: Most and Least active school level
# most_active =   query.loc[query['counts'].idxmax()]
# least_active =  query.loc[query['counts'].idxmin()]



# ## -- INDICATORS: Total Enrollees
# count_shs_school = shs_df['beis_id'].nunique()
# total_shs_enrollees = shs_df['counts'].sum()
# total_shs_enrollees


# # # Ratio per Strand
# # total_enrollees_per_strand = shs_df.groupby('strand', as_index=False)['counts'].sum()
# # total_enrollees_per_strand['ratio'] = total_enrollees_per_strand['counts'] / total_shs_enrollees
# # total_enrollees_per_strand

# # academic_track_ratio = total_enrollees_per_strand[total_enrollees_per_strand['track'] == 'ACAD'].values.tolist()[0][2]

# # # Ratio per track
# # total_enrollees_per_track = shs_df[
# #                                 shs_df['strand'] == 'ACAD'
# #                             ].groupby('track', as_index=False)['counts'].sum()
# # total_enrollees_per_track['ratio'] = total_enrollees_per_track['counts'] / total_shs_enrollees
# # total_enrollees_per_track

# # filtered_non_acad = total_enrollees_per_strand[total_enrollees_per_strand['strand'] == 'NON ACAD'].values.tolist()[0]
# # total_enrollees_per_track.loc[len(total_enrollees_per_track)] = pd.Series(filtered_non_acad, index=total_enrollees_per_track.columns)
# # total_enrollees_per_track


# # avg_stem = shs_df[shs_df['track'] == 'STEM']['counts'].sum() / total_shs_enrollees
# # avg_stem

# # average_per_track = shs_df['track'].value_counts(normalize=True)
# # average_per_track

# # # Ploting
# # custom_colors = ['#00AD7F', '#E0E0E0']
# # explode = [0, 0.15]

# # track_ratio_per_track = go.Figure(
# #     data=[
# #         go.Pie(labels=total_enrollees_per_strand['strand'], 
# #                values=total_enrollees_per_strand['ratio'], 
# #                marker=dict(colors=custom_colors),
# #                pull=explode
# #     )]
# # )

# # # Layout configs
# # track_ratio_per_track.update_layout(
# #     autosize=True,
# #     margin={"l": 8, "r": 8, "t": 16, "b": 0},  # Optional: Adjust margins
# # )

# # ----------------------------------------------------------
# # School Distribution Across Sectors

@callback(
    Output('home_school_number_per_sector', 'figure'),
    Input("url", "pathname")
)
def update_graph(pathname):
    if pathname != "/":
        return dash.no_update

    BASE_DF = smart_filter({}, _engine=enrollment_db_engine)
    BASE_DF = BASE_DF[["sector", "counts"]]
    
    # Extract and group data
    grouped_by_sectors = BASE_DF.groupby("sector")
    sector_counts = grouped_by_sectors.size().reset_index(name="count")

    # Create bar chart
    home_school_number_per_sector = px.bar(
        sector_counts,
        x="sector",
        y="count",
        text="count",
        orientation="v"
    )

    home_school_number_per_sector.update_traces(
        textposition="outside",
        marker_color="#037DEE"
    )

    home_school_number_per_sector.update_layout(
        autosize=True,
        margin={"l": 10, "r": 10, "t": 10, "b": 10},
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, showticklabels=True)
    )

    # Patch
    sector_patch = Patch()
    sector_patch["data"] = home_school_number_per_sector.data
    sector_patch["layout"] = home_school_number_per_sector.layout

    # Return inside callback
    return sector_patch


# # ----------------------------------------------------------


@callback(
    Output('home_gender_distribution', 'figure'),
    Input("url", "pathname")
)
def update_graph(pathname):
    if pathname != "/":
        return dash.no_update

    BASE_DF = smart_filter({}, _engine=enrollment_db_engine)
    BASE_DF = BASE_DF[['gender', 'counts']]

    # Group data
    grouped_by_gender = BASE_DF.groupby(['gender'], as_index=False)['counts'].sum()
    colors = ['#FF5B72', '#5DB7FF']

    # Create half-donut chart
    gender_fig = go.Figure(go.Pie(
        labels=grouped_by_gender['gender'],
        values=grouped_by_gender['counts'],
        hole=0.70,
        direction='clockwise',
        sort=False,
        textfont=dict(size=12, color='black'),
        marker=dict(colors=colors)
    ))

    # Update layout
    gender_fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        annotations=[dict(
            text='Gender<br>Distribution',
            x=0.5,
            y=0.5,
            font=dict(color='#3C6382', size=15),
            align='center',
            showarrow=False
        )],
    )
    gender_fig.update_traces(rotation=180)

    # Format counts
    total_male_count = grouped_by_gender.loc[grouped_by_gender['gender'] == 'M', 'counts'].values[0]
    total_female_count = grouped_by_gender.loc[grouped_by_gender['gender'] == 'F', 'counts'].values[0]

    # total_male_count_formatted = smart_truncate_number(total_male_count)
    # total_female_count_formatted = smart_truncate_number(total_female_count)

    # Calculate gender gap
    if total_male_count > total_female_count:
        gender_gap = ((total_male_count - total_female_count) / total_female_count) * 100
        # greater_gender = "MALE"
        # lesser_gender = "FEMALE"
    elif total_female_count > total_male_count:
        gender_gap = ((total_female_count - total_male_count) / total_male_count) * 100
        # greater_gender = "FEMALE"
        # lesser_gender = "MALE"
    else:
        gender_gap = 0
        # greater_gender = lesser_gender = "EQUAL"

    gender_gap = round(gender_gap, 2)

    # Patch the figure
    patched_gender_fig = Patch()
    patched_gender_fig["data"] = gender_fig.data
    patched_gender_fig["layout"] = gender_fig.layout

    # Return patch in callback
    return patched_gender_fig




# # ----------------------------------------------------------
# # Regional Distribution


@callback(
    Output('home_regional_distribution', 'figure'),
    Input("url", "pathname")
)
def update_graph(pathname):
    if pathname != "/":
        return dash.no_update

    BASE_DF = smart_filter({}, _engine=enrollment_db_engine)
    BASE_DF = BASE_DF[['region', 'counts']]
    
    # Extract and process data
    enrollees_per_region = BASE_DF.groupby(['region'], as_index=False)["counts"].sum()
    enrollees_per_region["counts_label"] = enrollees_per_region["counts"].apply(smart_truncate_number)

    # Define consistent region order
    ordered_regions = [
        'Region I', 'Region II', 'Region III', 'Region IV-A', 'Region IV-B',
        'Region V', 'Region VI', 'Region VII', 'Region VIII', 'Region IX',
        'Region X', 'Region XI', 'Region XII', 'CAR', 'NCR', 'CARAGA',
        'BARMM', 'PSO'
    ]
    enrollees_per_region['region'] = pd.Categorical(
        enrollees_per_region['region'],
        categories=ordered_regions,
        ordered=True
    )
    enrollees_per_region = enrollees_per_region.sort_values('region').reset_index(drop=True)

    # Create bar chart
    home_regional_distribution = px.bar(
        enrollees_per_region,
        x="region",
        y="counts",
        text="counts_label"
    )

    home_regional_distribution.update_traces(
        marker_color="#037DEE",
        textposition='outside',
        cliponaxis=False,
        textfont=dict(size=8, color="#04508c"),
        hovertemplate='Region: %{x}<br>Enrollees: %{y}',
    )

    home_regional_distribution.update_layout(
        autosize=True,
        margin={"l": 8, "r": 8, "t": 8, "b": 8},
        plot_bgcolor='#ECF8FF',
        yaxis=dict(
            automargin=True,
            title=None,
            showgrid=True,
            gridcolor='#D2EBFF',
            zeroline=False,
            tickfont=dict(size=8, color="#9DADBD")
        ),
        xaxis=dict(
            automargin=True,
            title=None,
            tickangle=-45,
            tickfont=dict(size=8, color="#9DADBD")
        ),
    )

    # Patch
    region_patch = Patch()
    region_patch["data"] = home_regional_distribution.data
    region_patch["layout"] = home_regional_distribution.layout

    # Return in callback
    return region_patch



# # ----------------------------------------------------------

@callback(
    # Output('home_shs_tracks', 'figure'),
    Output('ssc-subclass-table', 'figure'),
    Input("url", "pathname")
)
def update_graph(pathname):
    if pathname != "/":
        return dash.no_update

    BASE_DF = smart_filter({}, _engine=enrollment_db_engine)
    BASE_DF = BASE_DF[['beis_id', 'sub_class', 'counts']]
    
    subclass_df1 = (
        BASE_DF.groupby(['sub_class'])
        .agg(
            school_count=('beis_id', 'nunique'),
            counts=('counts', 'sum'),
        )
        .reset_index()
    )

    # # ---------- Chart ----------
    # home_subclass_chart = px.bar(
    #     subclass_df1,
    #     x='school_count',
    #     y='sub_class',
    #     orientation='h',
    #     text='school_count',
    #     color='sub_class',
    #     color_discrete_sequence=px.colors.qualitative.Set2
    # )

    # home_subclass_chart.update_traces(
    #     textposition='outside',
    #     marker_line_width=0.5,
    #     marker_line_color='gray'
    # )

    # home_subclass_chart.update_layout(
    #     title='Number of Schools per Subclassification',
    #     xaxis_title='Number of Schools',
    #     yaxis_title=None,
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     paper_bgcolor='rgba(0,0,0,0)',
    #     margin=dict(l=80, r=20, t=50, b=20),
    #     yaxis=dict(
    #         tickfont=dict(size=10, color='#4A4A4A')
    #     ),
    #     xaxis=dict(
    #         tickfont=dict(size=10, color='#4A4A4A'),
    #         gridcolor='#EDEDED',
    #         showgrid=True,
    #         zeroline=False
    #     ),
    #     showlegend=False
    # )

    # ---------- Table ----------
    home_subclass_table = go.Figure(data=[go.Table(
        columnwidth=[2, 1, 1],
        header=dict(
            values=["<b>Subclassification</b>", "<b>School Count</b>", "<b>Student Count</b>"],
            fill_color='#E6F2FB',
            font=dict(color='#04508c', size=12, family="Arial"),
            align='left',
            line_color='#B0C4DE',
            height=28
        ),
        cells=dict(
            values=[
                subclass_df1['sub_class'],
                subclass_df1['school_count'],
                subclass_df1['counts']
            ],
            fill_color=[['#FFFFFF', '#F7FAFC'] * (len(subclass_df1) // 2 + 1)],
            font=dict(color='#3C6382', size=11, family="Arial"),
            align='left',
            line_color='#D3D3D3',
            height=24
        )
    )])

    home_subclass_table.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    # # ---------- Patch Outputs ----------
    # chart_patch = Patch()
    # chart_patch["data"] = home_subclass_chart.data
    # chart_patch["layout"] = home_subclass_chart.layout

    table_patch = Patch()
    table_patch["data"] = home_subclass_table.data
    table_patch["layout"] = home_subclass_table.layout

    # Return them from your callback
    return table_patch


# # ----------------------------------------------------------
# # Ratio of Schools by Program Offering


@callback(
    Output('home_program_offering', 'figure'),
    Input("url", "pathname")
)
def update_graph(pathname):
    if pathname != "/":
        return dash.no_update

    BASE_DF = smart_filter({}, _engine=enrollment_db_engine)
    BASE_DF = BASE_DF[['mod_coc', 'counts']]
    
    # Extract and group
    grouped_by_offering = BASE_DF.groupby("mod_coc").size().reset_index(name="counts")

    # Flags for outer donut totals
    grouped_by_offering['has_ES'] = grouped_by_offering['mod_coc'].str.contains('ES', case=False, na=False) | \
                                    grouped_by_offering['mod_coc'].str.contains('All Offering', case=False, na=False)
    grouped_by_offering['has_JHS'] = grouped_by_offering['mod_coc'].str.contains('JHS', case=False, na=False) | \
                                    grouped_by_offering['mod_coc'].str.contains('All Offering', case=False, na=False)
    grouped_by_offering['has_SHS'] = grouped_by_offering['mod_coc'].str.contains('SHS', case=False, na=False) | \
                                    grouped_by_offering['mod_coc'].str.contains('All Offering', case=False, na=False)

    # Program totals
    es_total = grouped_by_offering.loc[grouped_by_offering['has_ES'], 'counts'].sum()
    jhs_total = grouped_by_offering.loc[grouped_by_offering['has_JHS'], 'counts'].sum()
    shs_total = grouped_by_offering.loc[grouped_by_offering['has_SHS'], 'counts'].sum()

    program_totals = pd.DataFrame({
        'program': ['ES', 'JHS', 'SHS'],
        'total_count': [es_total, jhs_total, shs_total]
    })

    outer_labels = program_totals['program']
    outer_values = program_totals['total_count']
    outer_color_map = {'ES': '#037DEE', 'JHS': '#FE4761', 'SHS': '#FFBF5F'}
    outer_colors = outer_labels.map(outer_color_map)

    # Pull the smallest slice
    smallest_outer_idx = outer_values.idxmin()
    outer_pull = [0] * len(outer_values)
    outer_pull[smallest_outer_idx] = 0.1

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

    # Build figure
    home_program_offering = go.Figure()

    # Outer ring (Programs)
    home_program_offering.add_trace(go.Pie(
        labels=outer_labels,
        values=outer_values,
        hole=0.7,
        direction='clockwise',
        sort=False,
        textinfo='none',
        pull=outer_pull,
        marker=dict(colors=outer_colors, line=dict(color='#3C6382', width=0)),
        domain={'x': [0, 1], 'y': [0, 1]},
        name='Programs',
        legendgroup='Program Offering',
        showlegend=True
    ))

    # Inner ring (Detailed Offerings)
    home_program_offering.add_trace(go.Pie(
        labels=inner_labels,
        values=inner_values,
        hole=0.43,
        direction='clockwise',
        rotation=90,
        sort=False,
        textinfo='none',
        marker=dict(colors=inner_colors, line=dict(color='#3C6382', width=0)),
        domain={'x': [0.22, 0.78], 'y': [0.22, 0.78]},
        name='Level',
        legendgroup='Education Level',
        showlegend=True
    ))

    # Layout
    home_program_offering.update_layout(
        showlegend=True,
        autosize=True,
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.05
        )
    )

    # Patch
    program_patch = Patch()
    program_patch["data"] = home_program_offering.data
    program_patch["layout"] = home_program_offering.layout

    # Return in callback
    return program_patch


# # ----------------------------------------------------------
# # Senior High School Tracks Distribution

@callback(
    Output('home_shs_tracks', 'figure'),
    Input("url", "pathname")
)
def update_graph(pathname):
    if pathname != "/":
        print("wrongness??")
        return dash.no_update

    BASE_DF = smart_filter({}, _engine=enrollment_db_engine)
    BASE_DF = BASE_DF[['track', 'counts']]
    
    # Extract and group data
    grouped_by_tracks = BASE_DF.groupby(["track"], as_index=False)["counts"].sum()
    grouped_by_tracks['counts_truncated'] = grouped_by_tracks['counts'].apply(smart_truncate_number)

    # Create bar chart
    home_shs_tracks = px.bar(
        grouped_by_tracks,
        x="track",
        y="counts",
        color="track",
        text="counts_truncated",
        color_discrete_sequence=["#B4162D", "#D61B35", "#E63E56", "#EA6074"]
    )

    # Update layout
    home_shs_tracks.update_layout(
        autosize=True,
        margin=dict(t=10, b=10, l=10, r=10),
        plot_bgcolor='#ECF8FF',
        showlegend=False,
        xaxis=dict(
            tickfont=dict(size=8, color="#3C6382"),
            title=None,
            showgrid=False,
        ),
        yaxis=dict(
            tickfont=dict(size=8, color="#3C6382"),
            title=None,
            showgrid=True,
            gridcolor='#D2EBFF',
            ticksuffix="  ",
        ),
    )

    # Update traces
    home_shs_tracks.update_traces(
        textposition='outside',
        insidetextanchor='middle',
        textfont=dict(size=8, color="#04508c"),
        hovertemplate='Track: %{x}<br>Count: %{y}<extra></extra>',
    )

    # Wrap in a Patch
    patched_shs_tracks = Patch()
    patched_shs_tracks["data"] = home_shs_tracks.data
    patched_shs_tracks["layout"] = home_shs_tracks.layout

    # Return this inside a callback
    return patched_shs_tracks



# # ----------------------------------------------------------


@callback(
    Output('home_shs_strands', 'figure'),
    Input("url", "pathname"),
)
def update_graph(pathname):
    time.sleep(1)
    if pathname != "/":
        return dash.no_update

    BASE_DF = smart_filter({}, _engine=enrollment_db_engine)
    BASE_DF = BASE_DF[['strand', 'counts']]

    # Data extraction and cleaning
    BASE_DF = BASE_DF[BASE_DF['strand'] != '__NaN__']

    # Group and sort
    grouped_by_strands = BASE_DF.groupby(["strand"], as_index=False)["counts"].sum()
    grouped_by_strands = grouped_by_strands.sort_values(by="counts", ascending=False)
    grouped_by_strands["category"] = "SHS Strands"

    # Create horizontal stacked bar chart
    home_shs_strands = px.bar(
        grouped_by_strands,
        x="counts",
        y="category",
        color="strand",
        orientation="h",
        text="counts",
        hover_name="strand",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )

    # Update layout
    home_shs_strands.update_layout(
        barmode='stack',
        height=None,
        width=None,
        autosize=True,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=8, color="#3C6382"),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=False,
            title=None,
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=False,
            title=None,
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='center',
            x=0.5,
            title=None,
        )
    )

    # Update traces
    home_shs_strands.update_traces(
        textposition='inside',
        insidetextanchor='middle',
        customdata=grouped_by_strands[["strand"]],
        hovertemplate='Strand: %{hovertext}<br>Count: %{x}<extra></extra>',
    )

    # Wrap in Patch
    patched_shs_strands = Patch()
    patched_shs_strands["data"] = home_shs_strands.data
    patched_shs_strands["layout"] = home_shs_strands.layout

    # Return inside callback
    return patched_shs_strands

