import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm
from sqlalchemy.orm import object_session
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError

Base = declarative_base()


class DBConnection():
    def __init__(self,db_filename='pst.db'):
        self.engine = create_engine('sqlite:///'+db_filename)
        Base.metadata.create_all(self.engine)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

class ProcessType(Base):
    __tablename__ = 'process_type'
    id = Column(Integer,primary_key=True)
    filepath = Column(String(250),nullable=False)

class Process(Base):
    __tablename__ = 'process'
    id = Column(Integer,primary_key=True)
    filename = Column(String(250), nullable=False)
    process_id = Column(Integer,nullable=False)
    title = Column(String(250), nullable=False)
    process_type_id = Column(Integer,ForeignKey(ProcessType.id))
    process_type = relationship(ProcessType)
    def __init__(self, filename,process_id,title,session):
        self.filename = filename
        self.process_id = process_id
        self.title = title
        try:
            process_type = session.query(ProcessType)\
                .filter(ProcessType.filepath == filename).one()
        except InvalidRequestError:
            print "createfilename"
            process_type = ProcessType(filepath=filename)
            session.add(process_type)
        self.process_type = process_type
        self.process_type_id = process_type.id
        print process_type.filepath

class Screenshot(Base):
    __tablename__ = 'screenshot'
    id = Column(Integer,primary_key=True)
    screen_id = Column(Integer,nullable=False)
    file_path = Column(String(250),nullable=False)
    time_taken = Column(DateTime,nullable=False)



