from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://postgres:8991Ngu#007@localhost:5432/postgres')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
    from sqlalchemy.orm import backref, relationship
    
    class Diabetes(Base):
        __tablename__ = 'diabetes'
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
    
    class Diabetes_Procedures(Base):
        __tablename__ = 'procedures'
        id = Column(Integer, primary_key=True)
        conf = Column(String)
        procedure = Column(String)
        
    class Liver(Base):
        __tablename__ = 'liver'
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
        
    p1 = Diabetes_Procedures(conf='55', procedure="p1")
    db_session.add(p1)
    p2 = Diabetes_Procedures(conf='60', procedure="p2")
    db_session.add(p2)
    p3 = Diabetes_Procedures(conf='65', procedure="p3")
    db_session.add(p3)
    p4 = Diabetes_Procedures(conf='70', procedure="p4")
    db_session.add(p4)
    p5 = Diabetes_Procedures(conf='75', procedure="p5")
    db_session.add(p5)
    p6 = Diabetes_Procedures(conf='80', procedure="p6")
    db_session.add(p6)
    p7 = Diabetes_Procedures(conf='85', procedure="p7")
    db_session.add(p7)
    p8 = Diabetes_Procedures(conf='90', procedure="p8")
    db_session.add(p8)
    p9 = Diabetes_Procedures(conf='95', procedure="p9")
    db_session.add(p9)
    p10 = Diabetes_Procedures(conf='100', procedure="p10")
    db_session.add(p10)
       
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    
    
    db_session.commit()

# init_db()