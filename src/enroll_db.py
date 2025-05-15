from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy import PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import project_root



### Create Engine for initializing the database of not yet existed
def initialize_db():
    engine = create_engine(f"sqlite:///{project_root / 'database/processed/sql/enrollment_data.db'}", echo=False)
    Base = declarative_base()

    class enrollment(Base):
        __tablename__ = 'enrollment'
    
        enroll_id = Column(Integer, primary_key=True, autoincrement=True)
        beis_id = Column(Integer)
        gender = Column(Enum('F', 'M'))


    class ES_enroll(Base):
        __tablename__ = 'ES_enroll'

        enroll_id = Column(Integer, ForeignKey('enrollment.enroll_id'), primary_key=True)
        grade = Column(String, primary_key=True)
        year = Column(Integer, primary_key=True)  # You *think* this is part of the key
        counts = Column(Integer)
            
    
    class JHS_enroll(Base):
        __tablename__ = 'JHS_enroll'
        
        enroll_id = Column(Integer, ForeignKey('enrollment.enroll_id'), primary_key=True)
        grade = Column(String, primary_key=True)   # Enumeration
        year = Column(Integer, primary_key=True)
        counts = Column(Integer)
        
    
    class SHS_enroll(Base):
        __tablename__ = 'SHS_enroll'
        
        enroll_id = Column(Integer, ForeignKey('enrollment.enroll_id'), primary_key=True)
        track = Column(String, primary_key=True)   # Enumeration
        strand = Column(String, primary_key=True)   # Enumeration
        grade = Column(String, primary_key=True)    # Enumeration
        year = Column(Integer, primary_key=True)
        counts = Column(Integer)

    
    class sch_info(Base):
        __tablename__ = 'sch_info'
        
        beis_id = Column(Integer, primary_key=True)
        name = Column(String)
        sector = Column(String)
        sub_class = Column(String)   # Enumeration
        type = Column(String) # Enumeration
        mod_coc = Column(String)     # Enumeration
        region_id = Column(Integer, ForeignKey('sch_region.region_id'))
        local_id = Column(Integer, ForeignKey('sch_local.local_id'))
        street = Column(String)
        
        
    class sch_region(Base):
        __tablename__ = 'sch_region'
        
        region_id = Column(Integer, primary_key=True, autoincrement=True)
        region = Column(String)   # Enumeration
        division = Column(String) # Enumeration
        district = Column(String) # Enumeration
        province = Column(String) # Enumeration
        
        
    class sch_local(Base):
        __tablename__ = 'sch_local'
        
        local_id = Column(Integer, primary_key=True, autoincrement=True)
        municipality = Column(String)
        legis_district = Column(String)
        brgy = Column(String)

    Base.metadata.create_all(engine)