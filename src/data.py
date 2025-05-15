from sqlalchemy import create_engine
import pandas as pd
import os, sys
from src.server import cache


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from config import project_root


"""
    INITIALIZING DATABASE CONNECTION AND CUSTOM FUNCTIONS:
    
"""

# Database Engine
enrollment_db_engine = create_engine(f"sqlite:///{project_root / 'database/processed/sql/enrollment_data.db'}", echo=False)
# print("DATABASE CALLED")

@cache.memoize(timeout=3600)
def smart_filter(filter_info={}, _engine=enrollment_db_engine) -> pd.DataFrame:
    try:
        # print("QUERYINGGG...")
        
        # Base query (JOIN: enrollment and sch_info)
        first_query = "SELECT * FROM enrollment LEFT JOIN sch_info USING(beis_id) WHERE 1=1"  
        params = {}
        
        first_scope = {
                'sector' : lambda x: f":sector_{x}",
                'sub_class' :lambda x: f":subclass_{x}",
                'type' :lambda x: f":type_{x}",
                'mod_coc' :lambda x: f":mod_coc_{x}"
        }
        
        second_scope = {
                'region' : lambda x: f":region_{x}",
                'province' :lambda x: f":province_{x}",
                'division' :lambda x: f":division_{x}",
                'district' :lambda x: f":district_{x}",
                'municipality' :lambda x: f":municipality_{x}",
                'brgy' :lambda x: f":district_{x}"
        }
        
        third_scope = {
                'grade' :lambda x: f":grade_{x}",
                'track' :lambda x: f":track_{x}",
                'strand' :lambda x: f":strand_{x}",
                'year' :lambda x: f":year_{x}",
        }
        
        
        # Check if there is column exist in the first_scope
        if any(key in filter_info for key in ['gender', 'sector', 'sub_class', 'type', 'mod_coc']):
            for col_key, value in filter_info.items():
                
                if col_key in ['sector', 'sub_class', 'type']:
                    ## Multiples
                    placeholders = ', '.join([first_scope[col_key](i) for i in range(len(value))])
                    params = {**params, **{first_scope[col_key](i)[1:]: v for i, v in enumerate(value)}}

                    first_query += f"\nAND {col_key} IN ({placeholders})"
                        
                if col_key in ['gender']:
                    ## Single
                    first_query += f"\nAND gender == '{filter_info['gender']}'"
                
                if col_key in ['mod_coc']:
                    placeholders = ', '.join([first_scope[col_key](i) for i in range(len([value]))])
                    params = {**params, **{first_scope[col_key](i)[1:]: v for i, v in enumerate([value])}}

                    first_query += f"\nAND {col_key} IN ({placeholders})"
        
        # print(first_query)
        
        # JOIN: first_query + location detailes
        region_query = f"""SELECT * FROM (
            {first_query}
        ) LEFT JOIN sch_region USING (region_id)
        LEFT JOIN sch_local USING (local_id)
        WHERE 1=1
        """
        if any(key in filter_info for key in ['region', 'province', 'division', 'district', 'municipality', 'brgy']):
            for col_key, value in filter_info.items():
                if col_key in ['region', 'province', 'division', 'district', 'municipality', 'brgy']:
                    ## LOCATION
                    placeholders = ', '.join([second_scope[col_key](i) for i in range(len(value))])
                    print(placeholders)
                    params = {**params, **{second_scope[col_key](i)[1:]: v for i, v in enumerate(value)}}
                    print(params)
                    region_query += f"\nAND {col_key} IN ({placeholders})"
        
        
        ## JOIN: region_query + grade
        grade_query = """SELECT * FROM (
            SELECT enroll_id, beis_id, gender, '__NaN__' as track, '__NaN__' as strand, grade, counts, year FROM enrollment
            INNER JOIN ES_enroll USING(enroll_id)

            UNION ALL

            SELECT enroll_id, beis_id, gender, '__NaN__' as track, '__NaN__' as strand, grade, counts, year FROM enrollment 
            INNER JOIN JHS_enroll USING(enroll_id)

            UNION ALL

            SELECT enroll_id, beis_id, gender, track, strand, grade, counts, year FROM enrollment 
            INNER JOIN SHS_enroll USING(enroll_id)
        )
        WHERE 1=1"""
        
        if any(key in filter_info for key in ['grade', 'strand', 'track', 'year']):
            # is_there_grade = False
            for col_key, value in filter_info.items():
                if col_key in ['grade', 'strand', 'track', 'year']:
                    ## LOCATION
                    placeholders = ', '.join([third_scope[col_key](i) for i in range(len(value))])
                    params = {**params, **{third_scope[col_key](i)[1:]: v for i, v in enumerate(value)}}

                    grade_query += f"\nAND {col_key} IN ({placeholders})"
                # if col_key in ['grade']:
                #     is_there_grade = True
                    
        
        ## MAIN QUERY
        main_query = f"""
            SELECT beis_id, gender, name, sector, sub_class, type,
                mod_coc, region, province, division, district, municipality, 
                brgy, track, strand, grade, counts, year 
            FROM(
                {region_query}
            ) INNER JOIN (
                {grade_query}
            ) USING (enroll_id, beis_id, gender)
        """
        
        # print('DONED... ANG QUERY')
        # print(main_query)
        # print("params:\n", params)
        
        dataframe = pd.read_sql_query(main_query, con=_engine, params=params)
        
        # List of column names
        columns_to_convert = ['gender', 'sector', 'sub_class', 'type', 'mod_coc',
                              'region', 'province', 'division', 'district',
                              'track', 'strand', 'grade']  

        for col in columns_to_convert:
            dataframe[col] = dataframe[col].astype('category')
        
        # print('Pandarette finished...')
        return dataframe
        
    except Exception as e:
        print(f'error: {e}')
        

def get_engine():
    return enrollment_db_engine
    
    
    
if __name__ == '__main__':
    sample = {}
    
    df = smart_filter(sample)
    
    df = df[['region', 'counts']]
    
    df_grouped = df.groupby('region', as_index=False)['counts'].sum()
    
    