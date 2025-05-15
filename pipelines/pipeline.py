import os, sys
from pipelines.pipeline_utils import extract, transform, load
from pipelines.pipeline_utils import trans_to_enrollment, trans_to_es_enroll, trans_to_jhs_enroll, trans_to_shs_enroll, trans_to_sch_region, trans_to_sch_local, trans_to_sch_info
import pandas as pd
import time
from pipelines.log_store import log_messages

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import project_root


"""
    ETL PIPELINES MAIN PROCESS
    
"""


# Paths: Raw aata Path and Load Path
source_path = project_root / "database/raw"
destination_path = lambda x: project_root / f"database/processed/csv/{x}"


# Check all excel files that uploaded at source file
def mine_data():
    file_list = [
        file for file in os.listdir(source_path)
    ]
    print(file_list)


    # Run through all the stored flatfiles for updating the database
    for file in file_list:
        
        log_messages.clear()
        
        # EXTRACT THE DATA SOURCE: DB from "dataset/raw"
        extracted_df, syear   = extract(source_path / file)
        
        log_messages.append('\nDetected School Year...')
        log_messages.append(f'>>> S.Y. {syear} - {syear + 1}')
        

        # TRANSFORM THE EXTRACTED DATA ACCORDING TO ERD
        transformed_df = transform(extracted_df)    # Generalize transformation

        # -- Transform all necessary dataset
        enrollment_df   = trans_to_enrollment(transformed_df)
        log_messages.append("")  # optional blank line

        
        es_enroll_df    = trans_to_es_enroll(transformed_df, enrollment_df, syear)
        jhs_enroll_df   = trans_to_jhs_enroll(transformed_df, enrollment_df, syear)
        shs_enroll_df   = trans_to_shs_enroll(transformed_df, enrollment_df, syear)
        
        sch_region_df   = trans_to_sch_region(transformed_df)
        log_messages.append("")  # optional blank line

        
        sch_local_df    = trans_to_sch_local(transformed_df)
        log_messages.append("")  # optional blank line

        sch_info_df     = trans_to_sch_info(transformed_df, sch_region_df, sch_local_df)


        # LOAD THE CLEANED AND NOMALIZED DATASETS IN "dataset/processed"
        
        # load(enrollment_df, destination_path('enrollment.csv')) 
        load(es_enroll_df, destination_path('ES_enroll.csv'))   
        log_messages.append("")  # optional blank line
        
        
        load(jhs_enroll_df, destination_path('JHS_enroll.csv'))
        log_messages.append("")  # optional blank line
        
        
        load(shs_enroll_df, destination_path('SHS_enroll.csv')) 
        log_messages.append("")  # optional blank line

        # load(sch_region_df, destination_path('sch_region.csv')) 
        # load(sch_local_df, destination_path('sch_local.csv'))   
        load(sch_info_df, destination_path('sch_info.csv'))     
        log_messages.append("")  # optional blank line
        
        log_messages.append('')
        log_messages.append('')
        log_messages.append('')
        
        log_messages.append("SUCCESSFULLY READ!!!")