from datetime import datetime
import sqlalchemy
from py_files.database import Base#, init_db1
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship

class Diabetes(Base):
        __tablename__ = 'diabetes'
        __table_args__ = {'extend_existing': True} 
        id = Column(Integer, primary_key=True)
        patientid = Column(String)
        numberofpregnancies = Column(Integer)
        glucose = Column(String)
        bloodpressure = Column(String)
        skinthickness = Column(String)
        insulinlevel = Column(String)
        bodymassindex = Column(String)
        diabetespedigreefunction = Column(String)
        age = Column(Integer)
        result = Column(String)
        conf = Column(String)
        procedure = Column(String)
        lastupdatedat = Column(sqlalchemy.DateTime(timezone=False), server_default=sqlalchemy.sql.func.now())
    
class Liver(Base):
        __tablename__ = 'liver'
        __table_args__ = {'extend_existing': True} 
        id = Column(Integer, primary_key=True)
        patientid = Column(String)
        age = Column(Integer)
        totalbilirubin = Column(String)
        directbilirubin = Column(String)
        alkalinephosphotase = Column(String)
        alamineaminotransferase = Column(String)
        aspartateaminotransferase = Column(String)
        totalprotiens = Column(String)
        albumin = Column(String)
        albuminandglobulinratio = Column(String)
        gender = Column(String)
        result = Column(String)
        conf = Column(String)
        lastupdatedat = Column(sqlalchemy.DateTime(timezone=False), server_default=sqlalchemy.sql.func.now())
        
class Diabetes_Procedures(Base):
        __tablename__ = 'procedures'
        __table_args__ = {'extend_existing': True} 
        id = Column(Integer, primary_key=True)
        conf = Column(String)
        procedure = Column(String)