from numpy import append
from sqlalchemy import create_engine
import pandas as pd
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from config import project_root


"""
    AUTOMATICALLY JOINED THE TABLE FOR QUERYING PURPOSES
"""

def auto_extract(requested_columns:list, is_specific=True, distinct=False) -> pd.DataFrame:
    try:
        engine = create_engine(f"sqlite:///{project_root / 'database/processed/sql/enrollment_data.db'}", echo=False)
        
        GRADE_LIST = ['ES_enroll', 'JHS_enroll', 'SHS_enroll']
        grade_cols = ['es_grade', 'jhs_grade', 'shs_grade']
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
                INNER JOIN {grade} USING (enroll_id)
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
        print(">>>", ', '.join(target_cols))
        if len(all_g_query) == 0:
            main_query = sch_query(', '.join(target_cols) if is_specific else '*')
        else:
            grouped_grade = '\nUNION ALL\n'.join(all_g_query)
            main_query = f"""
                SELECT {is_distinct} {', '.join(target_cols) if is_specific else '*'} 
                FROM ({sch_query('*')})
                LEFT JOIN (
                    {grouped_grade}
                ) USING (enroll_id)
                WHERE grade IS NOT NULL
            """
        # print(main_query)
        
        dataframe = pd.read_sql_query(main_query, con=engine)
        return dataframe
        
    except Exception as e:
        print(f'error: {e}')
        
    
if __name__ == '__main__':
    df = auto_extract(['counts'], is_specific=True)