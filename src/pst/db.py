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

Base = declarative_base()


class DBConnection():
    def __init__(self, db_filename='pst.db'):
        self.engine = create_engine('sqlite:///' + db_filename)
        Base.metadata.create_all(self.engine)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

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


class ProcessType(Base):
    __tablename__ = 'process_type'
    id = Column(Integer, primary_key=True)
    filepath = Column(String(250), nullable=False)


class DBProcess(Base):
    __tablename__ = 'process'
    id = Column(Integer, primary_key=True)
    filename = Column(String(250), nullable=False)
    process_id = Column(Integer, nullable=False)
    title = Column(String(250), nullable=False)
    datetime = Column(DateTime, nullable=False)
    process_type_id = Column(Integer, ForeignKey(ProcessType.id))
    process_type = relationship(ProcessType)

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


class Screenshot(Base):
    __tablename__ = 'screenshot'
    id = Column(Integer, primary_key=True)
    screen_id = Column(Integer, nullable=False)
    file_path = Column(String(250), nullable=False)
    time_taken = Column(DateTime, nullable=False)



