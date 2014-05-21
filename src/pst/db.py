import os
import sys
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm
from sqlalchemy.orm import object_session
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.util import KeyedTuple

Base = declarative_base()


class DBConnection():
    def __init__(self, db_filename='pst.db'):
        self.engine = create_engine('sqlite:///' + db_filename)
        Base.metadata.create_all(self.engine)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        try:
            self.create_default_process_category()
        except:
            self.session.rollback()

    def add_process(self, process):
        processtoadd = DBProcess(filename=process.filename,
                                 process_id=process.id,
                                 title=process.title,
                                 session=self.session,
                                 datetime=datetime.datetime.now())
        self.session.add(processtoadd)
        self.session.commit()
        return processtoadd

    def add_screenshot(self, screenshot_id, screenshot_path):
        screenshot_to_add = Screenshot(screen_id=screenshot_id,
                                       file_path=screenshot_path,
                                       time_taken=datetime.datetime.now())
        self.session.add(screenshot_to_add)
        self.session.commit()
        return screenshot_to_add

    def get_screenshots(self):
        data = self.session.query(Screenshot).all()
        return data

    def get_processes(self):
        data = self.session.query(DBProcess,ProcessType,ProcessCategory)
        return data

    def create_default_process_category(self):
        process_category = ProcessCategory(id=0,title="unassigned")
        self.session.add(process_category)
        self.session.commit()

class ProcessCategory(Base):
    __tablename__ = 'process_category'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    def __repr__(self):
        return "<ProcessCategory('%s')>" % self.title

class ProcessType(Base):
    __tablename__ = 'process_type'
    id = Column(Integer, primary_key=True)
    filepath = Column(String(250), nullable=False)
    process_category_id = Column(Integer, ForeignKey(ProcessCategory.id),default=0)
    process_category = relationship(ProcessCategory)
    def __repr__(self):
        return "<ProcessType('%s')>" % self.filepath


class DBProcess(Base):
    __tablename__ = 'process'
    id = Column(Integer, primary_key=True)
    filename = Column(String(250), nullable=False)
    process_id = Column(Integer, nullable=False)
    title = Column(String(250), nullable=False)
    datetime = Column(DateTime, nullable=False)
    process_type_id = Column(Integer, ForeignKey(ProcessType.id))
    process_type = relationship(ProcessType,backref='process')

    def __init__(self, filename, process_id, title, session, datetime):
        self.filename = filename
        self.process_id = process_id
        self.title = title
        self.datetime = datetime
        try:
            process_type = session.query(ProcessType) \
                .filter(ProcessType.filepath == filename).one()
        except InvalidRequestError:
            print "createfilename"
            process_type = ProcessType(filepath=filename)
            session.add(process_type)
        self.process_type = process_type
        self.process_type_id = process_type.id
        print process_type.filepath
    def __repr__(self):
        return "<DBProcess('%s')>" % self.filename



class Screenshot(Base):
    __tablename__ = 'screenshot'
    id = Column(Integer, primary_key=True)
    screen_id = Column(Integer, nullable=False)
    file_path = Column(String(250), nullable=False)
    time_taken = Column(DateTime, nullable=False)

def row2dict(row):
    if (type(row)is KeyedTuple):
        d = {}
        firstrow = True
        for subrow in row:
            d[subrow.__tablename__] = {}
            for column in subrow.__table__.columns:
                if firstrow:
                    d[column.name] = str(getattr(subrow, column.name))
                else:
                    d[subrow.__tablename__][column.name] = str(getattr(subrow, column.name))
            firstrow = False
        return d
    else:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))

        return d



