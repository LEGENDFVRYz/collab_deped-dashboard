from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd
import numpy as np
import sqlite3 as sql
import re, os, sys
import logging
import time
from pipelines.log_store import log_messages


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import project_root


"""
    ETL PIPELINES UTILITIES
    
    -- Made to support pipeline.py to run the ETL process from the /database/raw
    -- All transformed datas will be loaded to /database/processed for analysis
    
"""

# Get the directory and create the log path
current_dir = Path(__file__).resolve().parent
log_path = current_dir / "logfile.log"


# -- Configure logging
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format="%(asctime)s: [%(levelname)s] %(message)s",  # format
)

# Initialize the mask (seperated by school level)
es_mask = [
    'K Male', 'G1 Male', 'G2 Male', 'G3 Male',
    'G4 Male', 'G5 Male', 'G6 Male', 'Elem NG Male',
    'K Female', 'G1 Female', 'G2 Female', 'G3 Female',
    'G4 Female', 'G5 Female', 'G6 Female', 'Elem NG Female'
]
jhs_mask = [
    'G7 Male', 'G8 Male', 'G9 Male', 'G10 Male', 'JHS NG Male',
    'G7 Female', 'G8 Female', 'G9 Female', 'G10 Female', 'JHS NG Female'
]
shs_mask = [
    'G11 ACAD ABM Male', 'G11 ACAD HUMSS Male', 'G11 ACAD STEM Male', 'G11 ACAD GAS Male', 'G11 ACAD PBM Male', 
    'G11 TVL Male', 'G11 SPORTS Male', 'G11 ARTS Male', 'G12 ACAD ABM Male', 'G12 ACAD HUMSS Male', 'G12 ACAD STEM Male', 
    'G12 ACAD GAS Male', 'G12 ACAD PBM Male', 'G12 TVL Male', 'G12 SPORTS Male', 'G12 ARTS Male',
    'G11 ACAD ABM Female', 'G11 ACAD HUMSS Female', 'G11 ACAD STEM Female', 'G11 ACAD GAS Female', 'G11 ACAD PBM Female', 
    'G11 TVL Female', 'G11 SPORTS Female', 'G11 ARTS Female', 'G12 ACAD ABM Female', 'G12 ACAD HUMSS Female', 'G12 ACAD STEM Female', 
    'G12 ACAD GAS Female', 'G12 ACAD PBM Female', 'G12 TVL Female', 'G12 SPORTS Female', 'G12 ARTS Female'
]

log_messages.clear()


# EXTRACTION PROCESS FUNCTION
def extract(file_path: Path) -> pd.DataFrame:
    """
    Function for Extracting Data: 
        this function is fixed for "DB" sheet in the excel file
    
    Args:
        file_path (str): path of the corresponding excel_file (main database)

    Returns:
        pd.DataFrame: returns a DataFrame of the excel_file
    """
    
    try:
        print('Extracting...')
        log_messages.append('Extracting...')
        
        # determine how much skiprows is needed for reading the file:
        df = pd.read_excel(file_path, nrows=100, engine='openpyxl')
        skip_row = 0
        
        # determine the file school year using file name: soon to cross check
        start_year_file = file_path.stem.split("-")[1][:4]
        start_year_file = int(start_year_file) - 1 if len(start_year_file) > 1 and start_year_file[1][:4].isdigit() else False

        sample_cols = {
                        'region', 'division', 'district', 'beis school id', 'school name',
                        'street address', 'province', 'municipality', 'legislative district',
                        'barangay', 'sector', 'school subclassification', 'school type', 'modified coc'
                    }

        for row, line in df.iterrows():
            count = sum(1 for item in line if str(item).lower() in sample_cols)
            if re.search(r"SY", str(line.iloc[0])):     # or line[0] or line['column_name']
                title_row = line.iloc[0]
                start_year = int(title_row.split("-")[1][:4]) - 1
            if count > 7:           # if we found the header, save and break the loop
                skip_row = row + 1      # row + 1, to know how much to skipped to automatically read the columns
                break
        
        valid_start_year = start_year if start_year == start_year_file else min(start_year, start_year_file)
        df = pd.read_excel(file_path, skiprows=skip_row) # Find the right table
        
    except Exception as e:
        logging.error(f'Failed to Extract the {file_path}: \n\t{e}')
    else:
        logging.info('Successfully Extracted!') # log if successful
        return df, valid_start_year



# TRANSFORMATION PROCESS FUNCTION
def transform(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    General Transformation: Goal is to make the "DB" in consistent and have 
                            valid values. Also, cleaning the database for
                            further transformation.
    Args:
        dataframe (pd.DataFrame): Extracted Dataframe

    Returns:
        pd.DataFrame
    """
    
    try:
        print('Transforming...')
        log_messages.append('Transforming...')
        # Consistency of Naming Format: Renaming and standardization
        temp_df = dataframe.rename(columns={
            "Region": "region",
            "Division": "division",
            "District": "district",
            "Province": "province",
            "Municipality": "municipality",
            "Legislative District": "legis_district",
            "Barangay": "brgy",
            
            # Make is same to other columns
            "G11 ACAD - ABM Male": "G11 ACAD ABM Male",
            "G11 ACAD - ABM Female": "G11 ACAD ABM Female",
            "G11 ACAD - HUMSS Male": "G11 ACAD HUMSS Male",
            "G11 ACAD - HUMSS Female": "G11 ACAD HUMSS Female",
            "G12 ACAD - ABM Male": "G12 ACAD ABM Male",
            "G12 ACAD - ABM Female": "G12 ACAD ABM Female",
            "G12 ACAD - HUMSS Male": "G12 ACAD HUMSS Male",
            "G12 ACAD - HUMSS Female": "G12 ACAD HUMSS Female",
        })
        
        # Setting null values for out of scope values (based on their school level)
        temp_df.loc[~temp_df['Modified COC'].isin(['Purely ES', 'All Offering', 'ES and JHS']), es_mask] = np.nan
        temp_df.loc[~temp_df['Modified COC'].isin(['Purely JHS', 'JHS with SHS', 'All Offering', 'ES and JHS']), jhs_mask] = np.nan
        temp_df.loc[~temp_df['Modified COC'].isin(['Purely SHS', 'JHS with SHS', 'All Offering']), shs_mask] = np.nan
        
        # Set the a standard "NaN" in the brgy section for creating local_id in the furure
        temp_df.loc[:, 'brgy'] = temp_df['brgy'].fillna("__NaN__")
        
    except Exception as e:
        logging.error(f'Failed to Transform Data - Generalization: \n\t{e}')
    else:
        logging.info('Successfully Transformed!') # Log if successful
        return temp_df


# -- Transformation Func: Enrollment Table
def trans_to_enrollment(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Part of Transformation Process: Creating the "Enrollment" Table

    Args:
        dataframe (pd.DataFrame): import the transformed table in general

    Returns:
        pd.DataFrame: 
    """
    
    try:
        print('Transforming... enrollment dataframe')
        log_messages.append('Transforming... enrollment dataframe')
        
        temp_df = dataframe[['BEIS School ID']]
        
        # create new dataframe with combination of (beis, gender)
        enrollment_df = pd.DataFrame({
            'beis_id': list(temp_df['BEIS School ID']) * 2,
            'gender':  ['M', 'F'] * len(temp_df[['BEIS School ID']])
        })

        # # sort before making surrogate key
        # enrollment_df = enrollment_df.sort_values('beis_id').reset_index(drop=True)
        # enrollment_df = enrollment_df.reset_index(names='enroll_id')
        
        # change the datatype to category: gender
        enrollment_df['gender'] = enrollment_df['gender'].astype('str')
        
        # Sync all the surrogate key:
        engine = create_engine(f"sqlite:///{project_root / 'database/processed/sql/enrollment_data.db'}", echo=False)
        load(enrollment_df, project_root / f"database/processed/csv/enrollment.csv")
        
        new_enrollment_df = pd.read_sql('enrollment', con=engine)
        enrollment_df = enrollment_df.merge(new_enrollment_df, on=['beis_id', 'gender'], how='inner')
        
    except Exception as e:
        logging.error(f'Failed to Transform Data (enrollment) - Generalization: \n\t{e}')
    else:
        logging.info('-- Successfully Transformed further (enrollment table)!') # Log if successful
        return enrollment_df
    

# -- Transformation Func: ES_enroll Table
def trans_to_es_enroll(dataframe: pd.DataFrame, enrollment_df: pd.DataFrame, start_year: int) -> pd.DataFrame:
    """
    Part of Transformation Process: Creating the "ES_enroll" Table

    Args:
        dataframe (pd.DataFrame): import the transformed table in general
        enrollment_df (pd.DataFrame): import the enrollment table to sync the primary key
        start_year: reference for school year of the file (start year only)

    Returns:
        pd.DataFrame: 
    """
    
    m_es_mask = ['BEIS School ID'] + [
        x for x in es_mask if re.search(r'Male$', x)
    ]
    
    f_es_mask = ['BEIS School ID'] + [
        x for x in es_mask if re.search(r'Female$', x)
    ]
    
    try:
        print('Transforming... ES_enroll dataframe')
        log_messages.append('Transforming... ES_enroll dataframe')
        
        #-- Getting the male elem to jhs
        temp_df = dataframe[m_es_mask]
        male_es_enroll_df = temp_df.melt(  # Melt (Un-pivot) the grade column in DB
            id_vars=['BEIS School ID'],
            value_vars=m_es_mask[1:],
            var_name='grade',
            value_name='counts'
        )
        male_es_enroll_df['gender'] = 'M'  # declare it as "MALE"
        male_es_enroll_df['grade'] = male_es_enroll_df['grade'].str.split(' ').str[0]
        male_es_enroll_df.dropna(subset=['counts'], inplace=True)
        
        #-- Getting the female elem to jhs
        temp_df = dataframe[f_es_mask]
        female_es_enroll_df = temp_df.melt( # Melt (Un-pivot) the grade column in DB
            id_vars=['BEIS School ID'],
            value_vars=f_es_mask[1:],
            var_name='grade',
            value_name='counts'
        )
        female_es_enroll_df['gender'] = 'F'  # declare it as "FEMALE"
        female_es_enroll_df['grade'] = female_es_enroll_df['grade'].str.split(' ').str[0]
        female_es_enroll_df.dropna(subset=['counts'], inplace=True)
        # print(female_es_enroll_df.shape)
        
        #-- Combine both gender and get the corresponding enrollment key
        combined_df = pd.concat([male_es_enroll_df, female_es_enroll_df])
        combined_df = combined_df.sort_values(['BEIS School ID', 'gender'])

        # get the primary key (enroll_id) from enrollment_df
        es_enroll_df = combined_df.merge(enrollment_df, 
                                                left_on= ['BEIS School ID', 'gender'],
                                                right_on=['beis_id', 'gender']
                                            )
        es_enroll_df = es_enroll_df[['enroll_id', 'grade', 'counts']]  # Filter the necessary columns
        
        # drop all NULL values and correct the data types
        es_enroll_df['counts'] = es_enroll_df['counts'].astype('int')
        es_enroll_df['grade'] = es_enroll_df['grade'].astype('str')
        es_enroll_df['year'] = start_year
        es_enroll_df['year'] = es_enroll_df['year'].astype('int')
        
        # Standardizing the values (we could run similarity check in the future)
        es_enroll_df.loc[es_enroll_df['grade'].str.lower() == 'elem', 'grade'] = 'ES NG'

        
    except Exception as e:
        logging.error(f'Failed to Transform Data (ES_enroll) - Generalization: \n\t{e}')
    else:
        logging.info('-- Successfully Transformed further (ES_enroll table)!') # Log if successful
        return es_enroll_df
    

# -- Transformation Func: JHS_enroll Table
def trans_to_jhs_enroll(dataframe: pd.DataFrame, enrollment_df: pd.DataFrame, start_year: int) -> pd.DataFrame:
    """
    Part of Transformation Process: Creating the "JHS_enroll" Table

    Args:
        dataframe (pd.DataFrame): import the transformed table in general
        enrollment_df (pd.DataFrame): import the enrollment table to sync the primary key
        start_year: reference for school year of the file (start year only)
    
    Returns:
        pd.DataFrame: 
    """
    
    m_jhs_mask = ['BEIS School ID'] + [
        x for x in jhs_mask if re.search(r'Male$', x)
    ]
    
    f_jhs_mask = ['BEIS School ID'] + [
        x for x in jhs_mask if re.search(r'Female$', x)
    ]
    
    try:
        print('Transforming... JHS_enroll dataframe')
        log_messages.append('Transforming... JHS_enroll dataframe')
        
        
        #-- Getting the male elem to jhs
        temp_df = dataframe[m_jhs_mask]
        male_jhs_enroll_df = temp_df.melt(  # Melt (Un-pivot) the grade column in DB
            id_vars=['BEIS School ID'],
            value_vars=m_jhs_mask[1:],
            var_name='grade',
            value_name='counts'
        )
        male_jhs_enroll_df['gender'] = 'M'  # declare it as "MALE"
        male_jhs_enroll_df['grade'] = male_jhs_enroll_df['grade'].str.split(' ').str[0]

        
        #-- Getting the female elem to jhs
        temp_df = dataframe[f_jhs_mask]
        female_jhs_enroll_df = temp_df.melt( # Melt (Un-pivot) the grade column in DB
            id_vars=['BEIS School ID'],
            value_vars=f_jhs_mask[1:],
            var_name='grade',
            value_name='counts'
        )
        female_jhs_enroll_df['gender'] = 'F'  # declare it as "FEMALE"
        female_jhs_enroll_df['grade'] = female_jhs_enroll_df['grade'].str.split(' ').str[0]
        
        
        #-- Combine both gender and get the corresponding enrollment key
        combined_df = pd.concat([male_jhs_enroll_df, female_jhs_enroll_df])
        combined_df = combined_df.sort_values(['BEIS School ID', 'gender'])

        # get the primary key (enroll_id) from enrollment_df
        jhs_enroll_df = combined_df.merge(enrollment_df, 
                                                left_on= ['BEIS School ID', 'gender'],
                                                right_on=['beis_id', 'gender']
                                            )
        jhs_enroll_df = jhs_enroll_df[['enroll_id', 'grade', 'counts']]  # Filter the necessary columns
        
        # drop all NULL values and correct the data types
        jhs_enroll_df.dropna(subset=['counts'], inplace=True)
        jhs_enroll_df['counts'] = jhs_enroll_df['counts'].astype('int')
        jhs_enroll_df['grade'] = jhs_enroll_df['grade'].astype('str')
        jhs_enroll_df['year'] = start_year
        
        # Standardizing the values (we could run similarity check in the future)
        jhs_enroll_df.loc[jhs_enroll_df['grade'].str.lower() == 'jhs', 'grade'] = 'JHS NG'
        
    except Exception as e:
        logging.error(f'Failed to Transform Data (JHS_enroll) - Generalization: \n\t{e}')
    else:
        logging.info('-- Successfully Transformed further (JHS_enroll table)!') # Log if successful
        return jhs_enroll_df
    

# -- Transformation Func: SHS_enroll Table
def trans_to_shs_enroll(dataframe: pd.DataFrame, enrollment_df: pd.DataFrame, start_year: int) -> pd.DataFrame:
    """
    Part of Transformation Process: Creating the "SHS_enroll" Table

    Args:
        dataframe (pd.DataFrame): import the transformed table in general
        enrollment_df (pd.DataFrame): import the enrollment table to sync the primary key

    Returns:
        pd.DataFrame: 
    """
    m_shs_mask = [
        'BEIS School ID', 'G11 ACAD ABM Male', 'G11 ACAD HUMSS Male', 'G11 ACAD STEM Male', 'G11 ACAD GAS Male', 'G11 ACAD PBM Male', 
        'G11 TVL Male', 'G11 SPORTS Male', 'G11 ARTS Male', 'G12 ACAD ABM Male', 'G12 ACAD HUMSS Male', 'G12 ACAD STEM Male', 
        'G12 ACAD GAS Male', 'G12 ACAD PBM Male', 'G12 TVL Male', 'G12 SPORTS Male', 'G12 ARTS Male'
    ]
    f_shs_mask = [
        'BEIS School ID', 'G11 ACAD ABM Female', 'G11 ACAD HUMSS Female', 'G11 ACAD STEM Female', 'G11 ACAD GAS Female', 'G11 ACAD PBM Female', 
        'G11 TVL Female', 'G11 SPORTS Female', 'G11 ARTS Female', 'G12 ACAD ABM Female', 'G12 ACAD HUMSS Female', 'G12 ACAD STEM Female', 
        'G12 ACAD GAS Female', 'G12 ACAD PBM Female', 'G12 TVL Female', 'G12 SPORTS Female', 'G12 ARTS Female'
    ]
    
    try:
        print('Transforming... SHS_enroll dataframe...')
        log_messages.append('Transforming... SHS_enroll dataframe...')

        #-- Un-pivoting the male students 
        temp_df = dataframe[m_shs_mask]
        male_shs_enroll_df = temp_df.melt(
            id_vars=['BEIS School ID'],
            value_vars=m_shs_mask[1:],
            var_name='grade',
            value_name='counts'
        )
        male_shs_enroll_df['gender'] = 'M'  # declare it as "MALE"

        # get the track column
        male_shs_enroll_df['track'] = male_shs_enroll_df['grade'].apply(
            lambda x: x.split(' ')[1]
        )
        # get the strand column
        male_shs_enroll_df['strand'] = male_shs_enroll_df['grade'].apply(
            lambda x: x.split(' ')[2] if x.split(' ')[2] != 'Male' else '__NaN__'
        )
        male_shs_enroll_df['grade'] = male_shs_enroll_df['grade'].str.split(' ').str[0]
        
        
        # Un-pivoting the female students 
        temp_df = dataframe[f_shs_mask]
        female_shs_enroll_df = temp_df.melt(
            id_vars=['BEIS School ID'],
            value_vars=f_shs_mask[1:],
            var_name='grade',
            value_name='counts'
        )
        female_shs_enroll_df['gender'] = 'F'  # declare it as "FEMALE"

        # get the track column
        female_shs_enroll_df['track'] = female_shs_enroll_df['grade'].apply(
            lambda x: x.split(' ')[1]
        )

        # get the strand column
        female_shs_enroll_df['strand'] = female_shs_enroll_df['grade'].apply(
            lambda x: x.split(' ')[2] if x.split(' ')[2] != 'Female' else '__NaN__'
        )
        female_shs_enroll_df['grade'] = female_shs_enroll_df['grade'].str.split(' ').str[0]
        
        
        #-- Combine both gender and get the corresponding enrollment key
        combined_df = pd.concat([male_shs_enroll_df, female_shs_enroll_df])
        combined_df = combined_df.sort_values(['BEIS School ID', 'gender'])

        # get the primary key (enroll_id) from enrollment_df
        shs_enroll_df = combined_df.merge(enrollment_df, 
                                                left_on= ['BEIS School ID', 'gender'],
                                                right_on=['beis_id', 'gender']
                                            )

        # Filter the necessary columns
        shs_enroll_df = shs_enroll_df[['enroll_id', 'grade', 'strand', 'track', 'counts']]
        
        # drop all NULL values and correct the data types
        shs_enroll_df.dropna(subset=['counts'], inplace=True)
        shs_enroll_df = shs_enroll_df.astype({
            'counts': int,
            'grade': 'str',
            'strand': 'str',
            'track': 'str'
        })
        shs_enroll_df['year'] = start_year
        
        # Standardizing the values (we could run similarity check in the future)
        shs_enroll_df.loc[shs_enroll_df['track'].str.lower() == 'acad', 'track'] = 'ACADEMIC'
        
    except Exception as e:
        logging.error(f'Failed to Transform Data (SHS_enroll) - Generalization: \n\t{e}')
    else:
        logging.info('-- Successfully Transformed further (SHS_enroll table)!') # Log if successful
        return shs_enroll_df
    

# -- Transformation Func: sch_region Table
def trans_to_sch_region(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Part of Transformation Process: Creating the "sch_region" Table
    
    Args:
        dataframe (pd.DataFrame): Import the Generalized Transformed Data "DB"

    Returns:
        pd.DataFrame: 
    """
    try:
        print('Transforming... sch_region dataframe')
        log_messages.append('Transforming... sch_region dataframe')
        
        temp_df = dataframe[['region', 'division', 'district', 'province']].copy()
        
        # Standardizing the values (we could run similarity check in the future)
        temp_df.loc[temp_df['region'].str.lower() == 'mimaropa', 'region'] = 'Region IV-B'

        # Create a Primary Key for each combinations
        sch_region_df = temp_df.groupby(['region', 'province', 'division', 'district']).count().reset_index()
        # sch_region_df = sch_region_df.reset_index(names='region_id')
        
        # Sync all the surrogate key:
        engine = create_engine(f"sqlite:///{project_root / 'database/processed/sql/enrollment_data.db'}", echo=False)
        load(sch_region_df, project_root / f"database/processed/csv/sch_region.csv")
        
        new_region_df = pd.read_sql('sch_region', con=engine)
        new_record_df = sch_region_df.merge(new_region_df, on=['region', 'province', 'division', 'district'], how='inner')
        
    except Exception as e:
        logging.error(f'Failed to Transform Data (sch_region table) - Generalization: \n\t{e}')
        print(f'Failed to Transform Data (sch_region table) - Generalization: \n\t{e}')
        
    else:
        logging.info('-- Successfully Transformed further (sch_region table)!') # Log if successful
        log_messages.append('-- Successfully Transformed further (sch_region table)!')
        return new_record_df
    

# -- Transformation Func: sch_local Table
def trans_to_sch_local(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Part of Transformation Process: Creating the "sch_local" Table
    
    Args:
        dataframe (pd.DataFrame): Import the Generalized Transformed Data "DB"

    Returns:
        pd.DataFrame: 
    """
    try:
        print('Transforming... sch_local dataframe')
        log_messages.append('Transforming... sch_local dataframe')
        
        temp_df = dataframe[['municipality', 'legis_district', 'brgy']] 
        temp_df.loc[:, 'brgy'] = temp_df['brgy'].fillna("NaN")

        # Create a Primary Key for each combinations
        sch_local_df = temp_df.groupby(['municipality', 'legis_district', 'brgy']).count().reset_index()
        # sch_local_df = sch_local_df.reset_index(names='local_id')
        
        # Sync all the surrogate key:
        engine = create_engine(f"sqlite:///{project_root / 'database/processed/sql/enrollment_data.db'}", echo=False)
        load(sch_local_df, project_root / f"database/processed/csv/sch_local.csv")
        
        new_region_df = pd.read_sql('sch_local', con=engine)
        new_record_df = sch_local_df.merge(new_region_df, on=['municipality', 'legis_district', 'brgy'], how='inner')

    except Exception as e:
        logging.error(f'Failed to Transform Data (sch_local table) - Generalization: \n\t{e}')
        
    else:
        logging.info('-- Successfully Transformed further (sch_local table)!') # Log if successful
        return new_record_df
    

# -- Transformation Func: sch_region Table
def trans_to_sch_info(dataframe: pd.DataFrame, sch_region_df: pd.DataFrame, sch_local_df: pd.DataFrame) -> pd.DataFrame:
    """
    Part of Transformation Process: Creating the "sch_info" Table

    Args:
        dataframe (pd.DataFrame): Generalize Trandformed Data from "DB"
        sch_region_df (pd.DataFrame): import the clean sch_region table
        sch_local_df (pd.DataFrame): import the clean sch_local table

    Returns:
        pd.DataFrame: 
    """
    try:
        print('Transforming... sch_info...')
        log_messages.append('Transforming... sch_info...')
        
        
        temp_df = dataframe[['BEIS School ID', 'School Name', 'Sector', 'School Subclassification', 'School Type', 'Modified COC',
              'region', 'division', 'district', 'province', 'municipality', 'legis_district', 'brgy', 'Street Address']]
        
        # Standardizing the values (we could run similarity check in the future)
        temp_df.loc[temp_df['region'].str.lower() == 'mimaropa', 'region'] = 'Region IV-B'
        
        subclass_map = {
            'luc': 'LUC Managed',
            'school abroad': 'School Abroad',
            'deped managed': 'DepED Managed',
            'other ga managed': 'Other GA Managed',
            'dost managed': 'DOST Managed',
            'suc managed': 'SUC Managed',
            'non-sectarian': 'Non-Sectarian',
            'sectarian': 'Sectarian',
            'local international school': 'Local International School',
        }
        type_map = {
            'school with no annexes': 'No Annexes',
            'mother school': 'Mother School',
            'annex or extension school(s)': 'Annex/Extension',
            'mobile school(s)/center(s)': 'Mobile School'
        }
        
        # invalids street values
        invalids = [
            "", "none/na", "n/a", "0", "na", "(a)", "000000", "n / a", "0",
            "0000", "000000", "0000000", "00000000", "n /a", "n o n e",
            "n.a", "n.a.", "n/ a", "n\\a", "n/a none", "N/anone", "n/ad"
        ]

        # renaming the columns
        sch_info_df = temp_df.rename(columns={
            'BEIS School ID': 'beis_id', 
            'School Name': 'name', 
            'Sector': 'sector', 
            'School Subclassification': 'sub_class', 
            'School Type': 'type', 
            'Modified COC': 'mod_coc',
            'Street Address': 'street'
        })
        
        # Correcting the datatypes
        sch_info_df = sch_info_df.astype({
            'name': 'str',
            'sector': 'str', 
            'sub_class': 'str', 
            'type': 'str', 
            'mod_coc': 'str',
            'street': 'str',
        })
        
        # Remove trailing space and dash
        sch_info_df['street'] = sch_info_df['street'].str.strip(' -".')   
        sch_info_df['street'] = sch_info_df['street'].str.lstrip(' -*,.')
        sch_info_df['street'] = sch_info_df['street'].str.capitalize()
        
        # Standardizing the values (we could run similarity check in the future)
        sch_info_df['sub_class'] = sch_info_df['sub_class'].str.strip()
        sch_info_df['sub_class'] = sch_info_df['sub_class'].str.lower().replace(subclass_map)
        sch_info_df['type'] = sch_info_df['type'].str.lower().replace(type_map)
        
        sch_info_df.loc[sch_info_df['sector'].str.lower() == 'sucslucs', 'sector'] = 'SUCs/LUCs'
        
        
        valid_street_mask = (
            # making sure street has valid characters
            sch_info_df['street'].str.fullmatch(r"[^a-zA-Z0-9]+", na=False) |
            # filter out have variation of not ---
            sch_info_df['street'].str.contains(r"\s*not\s", case=False, na=False) |
            # filter out have variation of no ---
            sch_info_df['street'].str.contains(r"\s*no\s", case=False, na=False) |
            # filter out have variation of none ---
            sch_info_df['street'].str.contains(r"none\s*", case=False, na=False) |
            # filter out all have street name variations
            sch_info_df['street'].str.contains(r"street\s*name", case=False, na=False) |
            # filter out some outliers invalid format
            sch_info_df['street'].str.lower().isin(invalids)
        )
        sch_info_df.loc[valid_street_mask, 'street'] = np.nan

        # Make all null values have standard "NaN"
        sch_info_df['street'] = sch_info_df['street'].fillna("__NaN__")
        
        # inserting the "region_id" 
        sch_info_df = sch_info_df.merge(sch_region_df, on=['region', 'province', 'division', 'district'],  how='left')
        sch_info_df.drop(columns=['region', 'province', 'division', 'district'], inplace=True)

        # inserting the "local_id"
        sch_info_df = sch_info_df.merge(sch_local_df, on=['municipality', 'legis_district', 'brgy'], how='left')
        sch_info_df.drop(columns=['municipality', 'legis_district', 'brgy'], inplace=True)


    except Exception as e:
        logging.error(f'Failed to Transform Data (sch_info table) - Generalization: \n\t{e}')
    else:
        logging.info('-- Successfully Transformed further (sch_info table)!') # Log if successful
        return sch_info_df



# LOADING PROCESS FUNCTION
def load(dataframe: pd.DataFrame, path: Path):
    """
    LOAD PROCESS: Load the dataset into specified_path

    Args:
        dataframe (pd.DataFrame): Generalize Trandformed Data from "DB"
        path (Path): Path where to load the dataset
    """
    
    relative_path = path.relative_to(project_root) # For logging purposes

    # ### Load the data: CSV ########################################################## 
    # try:
    #     print(f'loading csv... {relative_path}')
    #     backup_path = path.parent / "backup" / f"--{path.stem}_backup{path.suffix}"
    #     dtype_map = dataframe.dtypes.apply(lambda x: x.name).to_dict()
        
    #     # Check if the file is already exist
    #     is_file_exist = os.path.exists(path) 
    #     if is_file_exist: 
    #         existing_df = pd.read_csv(path, dtype=dtype_map, low_memory=False) 
    #     else: 
    #         existing_df = None
        
        
    #     # # create back-up (one-instance of older version)
    #     # if os.path.exists(path):
    #     #     if os.path.exists(backup_path):
    #     #         os.unlink(backup_path)  # Delete the back-up first if exist
    #     #     os.rename(path,
    #     #         # Manipulated path directly to backup folder with appropriate naming standard
    #     #         # f"{'/'.join(path.split('/')[:-1])}/backup/--{path.split('/')[-1][:-4]}_backup.csv"
    #     #         backup_path
    #     #     )
        
    #     # # filter out the existing rows
    #     # if existing_df is not None:
    #     #     new_records_df = pd.concat([dataframe, existing_df]).drop_duplicates(keep=False)
    #     # else:
    #     #     new_records_df = dataframe
        
    #     new_records_df = pd.concat([dataframe, existing_df]).drop_duplicates(keep=False)
                
    # except Exception as e:
    #     print(f"FAILED: {relative_path} \n\t{e}")
    #     logging.error(f'Failed to Load CSV Data ({relative_path}) \n\t{e}')
    # else:
    #     new_records_df.to_csv(path, mode='a', header=(not is_file_exist), index=False)
    #     logging.info(f'-- Successfully load the CSV dataset: ({relative_path})') # Log if successful
    #     print(f'-- Successfully load the CSV dataset: (new {new_records_df.shape[0]} rows added) -> {relative_path})')
        
    
    ### Load the data: SQLite #######################################################
    try:
        print(f'loading sql... {relative_path}')
        log_messages.append(f'loading sql... {relative_path}')
        
        
        # # Key Mapping of Primary Keys
        # keys = {
        #     'enrollment': ['']
        # }
        
        # Database location
        engine = create_engine(f"sqlite:///{project_root / 'database/processed/sql/enrollment_data.db'}", echo=False)
        
        # Get the existing table to get new rows to be appended
        existing_df = pd.read_sql(path.stem, con=engine)
        
        # filter out the existing rows
        new_records_df = dataframe.merge(existing_df, how='left', indicator=True)
        new_records_df = new_records_df[new_records_df['_merge'] == 'left_only'].drop(columns=['_merge'])

        # print('\n=======================')
        # print(new_records_df)
        
        new_records_df.to_sql(path.stem, con=engine, index=False, if_exists='append')
        
        if not new_records_df.empty:
            df_preview = new_records_df.head().to_string(index=False)
            log_messages.append("")  # optional blank line
            log_messages.append(df_preview)
        else:
            log_messages.append("⚠️ DataFrame is empty — nothing to show.")
        
    except Exception as e:
        print(f"FAILED: {relative_path} \n\t{e}")
        logging.error(f'Failed to Load SQL table ({relative_path}) \n\t{e}')
        print(f'Failed to Load SQL table ({relative_path}) \n\t{e}')
    else:
        # Push all the new records        
        # new_records_df.to_sql(path.stem, con=engine, index=False, if_exists='append')
        logging.info(f'-- Successfully load the SQL table: (new {new_records_df.shape[0]} rows added) -> {relative_path})') # Log if successful
        print(f'-- Successfully load the SQL table: (new {new_records_df.shape[0]} rows added) -> {relative_path})\n')
        log_messages.append(f'-- Successfully load the SQL table: (new {new_records_df.shape[0]} rows added) -> {relative_path})\n')
        