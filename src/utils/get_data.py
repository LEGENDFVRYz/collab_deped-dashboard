from tkinter import font
from turtle import title
from numpy import append
from sqlalchemy import create_engine
import pandas as pd
import os, sys

import json
import os
import plotly.express as px
# from geojson_rewind import rewind
import pandas as pd
import plotly.io as pio


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from config import project_root


"""
    AUTOMATICALLY JOINED THE TABLE FOR QUERYING PURPOSES
"""

def auto_extract(requested_columns:list, is_specific=True, distinct=False) -> pd.DataFrame:
    try:
        engine = create_engine(f"sqlite:///{project_root / 'database/processed/sql/enrollment_data.db'}", echo=False)
        
        GRADE_LIST = ['ES_enroll', 'JHS_enroll', 'SHS_enroll']
        grade_cols = ['es_grade', 'jhs_grade', 'shs_grade', 'gender']
        is_distinct = ''
        
        data_record = {
            'enrollment': ['gender'],
            'ES_enroll':  ['es_grade'], 
            'JHS_enroll': ['jhs_grade'], 
            'SHS_enroll': ['shs_grade', 'strand', 'track'],
            'sch_info':   ['beis_id', 'name', 'sector', 'sub_class', 'type', 'mod_coc', 'street'],
            'sch_local':  ['municipality', 'legis_district', 'brgy'],
            'sch_region': ['region', 'division', 'province']
        }
        root_table = {
            'enrollment': ['enrollment', 'ES_enroll', 'JHS_enroll', 'SHS_enroll'],
            'sch_info':   ['sch_info', 'sch_region', 'sch_local']
        }
        data_keys = {
            'sch_local':  'local_id',
            'sch_region': 'region_id',
        }
        
        
        if 'counts' in requested_columns and all(col not in requested_columns for col in grade_cols[:3]):   # automatic all grade levels
            requested_columns += grade_cols[:3]
            
        if distinct:
            is_distinct = 'DISTINCT'
        
        # Determine the related tables to be merge based on requested columns
        related_table = []
        for table_name, ref_columns in data_record.items():
            if (set(requested_columns) & set(ref_columns)):
                related_table.append(table_name)
        
        
        # Determine the root table
        roots = []
        for root, ref_tables in root_table.items():
            if (set(related_table) & set(ref_tables)):
                roots.append(root)
        related_table = [t for t in related_table if t not in roots] # remove the root table in related
        
        
        ###### HANDLES THE JOINING THE GRADE DATA ########
        related_sch_table = [x for x in related_table if x not in GRADE_LIST]
        related_grade_table = [x for x in related_table if x in GRADE_LIST]
        
        # print(related_table)
        # print(related_grade_table)
        # print(roots)
        
        
        ###### HANDLES THE JOINING OF SCHOOL INFORMATION ########
        if related_sch_table:
            left_join = "\n".join([
                f"LEFT JOIN {t} USING ({data_keys[t]})"
                for t in related_sch_table
            ])
        else:
            left_join = ''
        
        ###### HANDLES THE CASES IF TWO ROOTS ONLY ########
        if set(roots) == set(["enrollment", "sch_info"]):
            roots = [
                "(SELECT * FROM enrollment LEFT JOIN sch_info USING (beis_id))"
            ]
        
        
        ### -- Grade Query
        all_g_query = []
        if len(related_grade_table) == 1 and related_grade_table[0] == 'SHS_enroll':
            ## If SHS only is selected
            all_g_query.append(f"""
                SELECT * FROM enrollment
                LEFT JOIN SHS_enroll USING (enroll_id)
            """)
        elif related_grade_table:
            ## multiple grade is selected
            for grade in related_grade_table:
                if grade == 'SHS_enroll':
                    cols = 'enroll_id,beis_id,gender,grade,counts,year'
                else:
                    cols = '*'
                    
                g_query = f"""
                SELECT {cols} FROM enrollment
                LEFT JOIN {grade} USING (enroll_id)
                """
                all_g_query.append(g_query)
                
        
        ### -- School Info Query
        for id in grade_cols:
            if id in requested_columns: requested_columns.append('grade'); break
        target_cols = [x for x in requested_columns if x not in grade_cols]
        
        sch_query = lambda x: f"""
            SELECT {is_distinct} {x}
            FROM {roots[0]}
            {
                left_join
            }
        """
        
        ### main query
        # print(">>>", ', '.join(target_cols))
        if len(all_g_query) == 0:
            main_query = sch_query(', '.join(target_cols) if is_specific else '*')
        else:
            grouped_grade = '\nUNION ALL\n'.join(all_g_query)
            main_query = f"""
                SELECT {is_distinct} {', '.join(target_cols) if is_specific else '*'} 
                FROM ({sch_query('*')})
                LEFT JOIN (
                    {grouped_grade}
                ) USING (enroll_id, beis_id, gender)
                WHERE grade IS NOT NULL
            """
        # print(main_query)
        
        dataframe = pd.read_sql_query(main_query, con=engine)
        return dataframe
        
    except Exception as e:
        print(f'error: SQL QUERY FAILED')
        
    
if __name__ == '__main__':
    # df = auto_extract(['region'], is_specific=False)
    df = auto_extract(['year', 'sub_class', 'counts'], is_specific=True)

    # # Grouped Line Chart
    # df_grouped = df.groupby(['year', 'sub_class'], as_index=False)['counts'].sum()

    # custom_colors = {
    # 'DOST Managed': '#4F0A14',
    # 'DepEd Managed': '#710E1C',
    # 'LUC Managed': '#921224',
    # 'Local International School': '#B4162D',
    # 'Non-Sectrian': '#D61B35',
    # 'Other GA Managed': '#E63E56',
    # 'SUC Managed': '#EA6074',
    # 'School Abroad': '#EF8292',
    # 'Sectarian': '#F3A4AF',
    # }


    # df_grouped['year'] = pd.Categorical(
    #     df_grouped['year'],
    #     categories=sorted(df_grouped['year'].unique()),
    #     ordered=True
    # )

    # fig = px.line(
    #     df_grouped,
    #     x='year',
    #     y='counts',
    #     color='sub_class',
    #     markers=True,
    #     title='Annual Enrollment Trends per Subclass',
    #     color_discrete_map=custom_colors,
    # )

    # fig.update_layout(
    #     title=dict(
    #         text='Annual Enrollment Trends per Subclass',
    #         font=dict(
    #             family= 'Inter Bold',
    #             size=20,
    #             color='#3C6382'
    #         ),
    #     ),
    #     xaxis_title='Year',
    #     yaxis_title='Total Enrollees',
    #     legend_title='Subclass'
    # )
    
    # # Line Chart with Percentage Change since Slope Chart wont show if only one year is available
    # df_grouped = df.groupby(['year', 'sub_class'], as_index=False)['counts'].sum()

    # df_grouped = df_grouped.sort_values(['sub_class', 'year'])
    # df_grouped['pct_change'] = df_grouped.groupby('sub_class')['counts'].pct_change() * 100

    # df_grouped['pct_change'] = df_grouped['pct_change'].fillna(0)

    # fig = px.line(
    #     df_grouped,
    #     x='year',
    #     y='pct_change',
    #     color='sub_class',
    #     markers=True,
    #     title='Annual Enrollment Growth Rate by School Subclassification',
    #     labels={'pct_change': 'Percent Change (%)'}
    # )

    # if df_grouped['year'].nunique() == 1:
    #     fig.update_layout(
    #         title={
    #             'text': 'Annual Enrollment Growth Rate by School Subclassification<br><sup>(Only one year available — growth set to 0%)</sup>',
    #             'x': 0.5
    #         }
    #     )

    # fig.update_layout(
    #     xaxis_title='Year',
    #     yaxis_title='Percent Change in Enrollment (%)',
    #     legend_title='Subclass'
    # )

    # #Slope Chart
    # df['year'] = df['year'].astype(str)

    # df_grouped = df.groupby(['year', 'sub_class'], as_index=False)['counts'].sum()

    # pivot_df = df_grouped.pivot(index='sub_class', columns='year', values='counts')

    # if pivot_df.shape[1] != 2:
    #     raise ValueError("Slope chart requires exactly two years of data.")

    # pivot_df = pivot_df.reset_index()
    # pivot_df_melted = pivot_df.melt(id_vars='sub_class', var_name='year', value_name='enrollment')

    # fig = px.line(
    #     pivot_df_melted,
    #     x='year',
    #     y='enrollment',
    #     color='sub_class',
    #     markers=True,
    #     line_group='sub_class',
    #     title='Enrollment % Change Between Two Years (Slope Chart)'
    # )

    # fig.update_layout(
    #     xaxis_title='Year',
    #     yaxis_title='Enrollment Count',
    #     legend_title='Subclass',
    #     showlegend=True
    # )


    # # Boxplot
    # df['year'] = df['year'].astype(str)  
    # df['sub_class'] = df['sub_class'].astype(str)  
 
    # df_grouped = df.groupby(['sub_class', 'year'], as_index=False)['counts'].sum()

    # custom_colors = {
    # 'DOST Managed': '#4F0A14',
    # 'DepEd Managed': '#710E1C',
    # 'LUC Managed': '#921224',
    # 'Local International School': '#B4162D',
    # 'Non-Sectrian': '#D61B35',
    # 'Other GA Managed': '#E63E56',
    # 'SUC Managed': '#EA6074',
    # 'School Abroad': '#EF8292',
    # 'Sectarian': '#F3A4AF',
    # }

    # fig = px.box(
    #     df_grouped,
    #     x='sub_class',
    #     y='counts',
    #     color='sub_class',
    #     title='Enrollment Spread by Subclassification',
    #     points='all',  
    #     labels={'counts': 'Total Enrollment', 'sub_class': 'School Subclassification'},
    #     color_discrete_map=custom_colors,
    # )

    # fig.update_layout(
    #     title_font_color='#3C6382',  
    #     # xaxis_title='School Subclassification',
    #     yaxis_title='Total Enrollment per Year',
    #     legend_title='Subclassification',
    #     font=dict(color='#667889'), 
    #     title_font=dict(color='#3C6382', size=20),
    # )

    # Grouped Line Chart
    df_grouped = df.groupby(['year', 'sub_class'], as_index=False)['counts'].sum()

    custom_colors = {
        'DOST Managed': '#4F0A14',
        'DepEd Managed': '#710E1C',
        'LUC Managed': '#921224',
        'Local International School': '#B4162D',
        'Non-Sectrian': '#D61B35',
        'Other GA Managed': '#E63E56',
        'SUC Managed': '#EA6074',
        'School Abroad': '#EF8292',
        'Sectarian': '#F3A4AF',
    }

    df_grouped['year'] = pd.Categorical(
        df_grouped['year'],
        categories=sorted(df_grouped['year'].unique()),
        ordered=True
    )

    fig = px.line(
        df_grouped,
        x='year',
        y='counts',
        color='sub_class',
        markers=True,
        title='Annual Enrollment Trends per Subclass',
        color_discrete_map=custom_colors,
    )

    fig.update_layout(
        title=dict(
            text='Annual Enrollment Trends per Subclass',
            font=dict(
                family='Inter Bold',
                size=20,
                color='#3C6382'
            ),
        ),
        xaxis_title=dict(
            text='Year',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        yaxis_title=dict(
            text='Total Enrollees',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        legend_title=dict(
            text='Subclass',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        font=dict(
            family='Inter',
            size=12,
            color='#667889'
        )
    )

    # Line Chart with Percentage Change
    df_grouped = df.groupby(['year', 'sub_class'], as_index=False)['counts'].sum()
    df_grouped = df_grouped.sort_values(['sub_class', 'year'])
    df_grouped['pct_change'] = df_grouped.groupby('sub_class')['counts'].pct_change() * 100
    df_grouped['pct_change'] = df_grouped['pct_change'].fillna(0)

    fig = px.line(
        df_grouped,
        x='year',
        y='pct_change',
        color='sub_class',
        markers=True,
        title='Annual Enrollment Growth Rate by School Subclassification',
        labels={'pct_change': 'Percent Change (%)'}
    )

    if df_grouped['year'].nunique() == 1:
        fig.update_layout(
            title={
                'text': 'Annual Enrollment Growth Rate by School Subclassification<br><sup>(Only one year available — growth set to 0%)</sup>',
                'x': 0.5,
                'font': dict(
                    family='Inter Bold',
                    size=20,
                    color='#3C6382'
                )
            }
        )

    fig.update_layout(
        xaxis_title=dict(
            text='Year',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        yaxis_title=dict(
            text='Percent Change in Enrollment (%)',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        legend_title=dict(
            text='Subclass',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        font=dict(
            family='Inter',
            size=12,
            color='#667889'
        )
    )

    # Slope Chart
    df['year'] = df['year'].astype(str)
    df_grouped = df.groupby(['year', 'sub_class'], as_index=False)['counts'].sum()
    pivot_df = df_grouped.pivot(index='sub_class', columns='year', values='counts')

    if pivot_df.shape[1] != 2:
        raise ValueError("Slope chart requires exactly two years of data.")

    pivot_df = pivot_df.reset_index()
    pivot_df_melted = pivot_df.melt(id_vars='sub_class', var_name='year', value_name='enrollment')

    fig = px.line(
        pivot_df_melted,
        x='year',
        y='enrollment',
        color='sub_class',
        markers=True,
        line_group='sub_class',
        title='Enrollment % Change Between Two Years (Slope Chart)'
    )

    fig.update_layout(
        title=dict(
            font=dict(
                family='Inter Bold',
                size=20,
                color='#3C6382'
            )
        ),
        xaxis_title=dict(
            text='Year',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        yaxis_title=dict(
            text='Enrollment Count',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        legend_title=dict(
            text='Subclass',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        font=dict(
            family='Inter',
            size=12,
            color='#667889'
        ),
        showlegend=True
    )

    # Boxplot
    df['year'] = df['year'].astype(str)
    df['sub_class'] = df['sub_class'].astype(str)
    df_grouped = df.groupby(['sub_class', 'year'], as_index=False)['counts'].sum()

    fig = px.box(
        df_grouped,
        x='sub_class',
        y='counts',
        color='sub_class',
        title='Enrollment Spread by Subclassification',
        points='all',
        labels={'counts': 'Total Enrollment', 'sub_class': 'School Subclassification'},
        color_discrete_map=custom_colors,
    )

    fig.update_layout(
        title=dict(
            font=dict(
                family='Inter Bold',
                size=20,
                color='#3C6382'
            )
        ),
        xaxis_title=dict(
            text='School Subclassification',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        yaxis_title=dict(
            text='Total Enrollment per Year',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        legend_title=dict(
            text='Subclassification',
            font=dict(
                family='Inter Medium',
                size=14,
                color='#667889'
            )
        ),
        font=dict(
            family='Inter',
            size=12,
            color='#667889'
        )
    )


