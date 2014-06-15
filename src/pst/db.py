#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy

import os
import sys
import datetime
import traceback

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, and_, update
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
        self.engine = create_engine('sqlite:///' + db_filename, echo=False)

        self.engine.raw_connection().connection.text_factory = str
        Base.metadata.create_all(self.engine)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
        self.current_process = None
        try:
            self.create_default_process_category()
        except:
            self.session.rollback()

    def add_process(self, process):
        now = datetime.datetime.now()
        processtoadd = DBProcess(filename=process.filename,
                                 process_id=process.id,
                                 title=process.title,
                                 session=self.session,
                                 start_time=now,
                                 end_time=now)
        try:
            if (self.current_process.filename == processtoadd.filename and
                self.current_process.title == processtoadd.title):

                self.current_process.end_time = now
                self.session.expunge(processtoadd)
                # processtoadd = None
                self.session.commit()

                return self.current_process
        except Exception, e:
            # print(repr(traceback.format_exc()))
            pass
        # print ("Adding Process")
        try:
            self.current_process.end_time = now
        except:
            pass
        self.session.add(processtoadd)
        self.session.commit()
        self.current_process = processtoadd
        # print ("Added Process")
        return processtoadd

    def add_screenshot(self, screenshot_id, screenshot_path):
        screenshot_to_add = Screenshot(screen_id=screenshot_id,
                                       file_path=screenshot_path,
                                       time_taken=datetime.datetime.now())
        self.session.add(screenshot_to_add)
        self.session.commit()
        return screenshot_to_add

    def add_category(self,title,title_search,filename_search):
        new_cat = ProcessCategory(title=title,
                                  title_search=title_search,
                                  filename_search=filename_search)
        self.session.add(new_cat)
        self.session.commit()
        return new_cat

    def get_screenshots(self):
        data = self.session.query(Screenshot).limit(100)
        return data

    def get_processes(self,start_time=None,end_time=None,pid=None):
        if start_time is None:
            start_time = 0
        if end_time is None:
            end_time = datetime.datetime.now()
        # data = self.session.query(DBProcess,ProcessType,ProcessCategory).order_by(DBProcess.datetime.desc()).limit(100)
        data = self.session.query(DBProcess,ProcessType,ProcessCategory)\
            .join(ProcessType)\
            .join(ProcessCategory)\
            .filter(and_(DBProcess.start_time <=end_time,DBProcess.start_time>=start_time))\
            .order_by(DBProcess.start_time.asc())\
            # .limit(100)
        # data = self.session.query(DBProcess,ProcessType).join(ProcessType).limit(10)
        if (pid):
            data = data.filter(DBProcess.id == pid)
        return data

    def get_process_categories(self):
        data = self.session.query(ProcessCategory)
        return data

    def create_default_process_category(self):
        process_category = ProcessCategory(id=0,title="unassigned")
        self.session.add(process_category)
        self.session.commit()

    def assign_categories(self):
        categories = self.session.query(ProcessCategory)
        # process_types = self.session.query(ProcessType)
        for category in categories:
            matched = self.session.query(ProcessType)\
                .filter(ProcessType.title.like("%{0}%".format(category.title_search)),
                        ProcessType.filepath.like("%{0}%".format(category.filename_search)))

            for match in matched:
                match.process_category = category

            # for process_type in process_types:
            #     if category.title_search.lower() in process_type.title.lower() and \
            #         category.filename_search.lower() in process_type.filepath.lower():
            #         process_type.process_category = category


        self.session.commit()



class ProcessCategory(Base):
    __tablename__ = 'process_category'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    title_search = Column(String(250), default='')
    filename_search = Column(String(250), default='')
    order = Column(Integer,default=0)
    def __repr__(self):
        return "<ProcessCategory('%s')>" % self.title

class ProcessType(Base):
    __tablename__ = 'process_type'
    id = Column(Integer, primary_key=True)
    filepath = Column(String(250), nullable=False)
    title = Column(String(250,convert_unicode=True), nullable=False)
    process_category_id = Column(Integer, ForeignKey(ProcessCategory.id),default=0)
    process_category = relationship(ProcessCategory)
    def __repr__(self):
        return "<ProcessType('%s')>" % self.filepath


class DBProcess(Base):
    __tablename__ = 'process'
    id = Column(Integer, primary_key=True)
    filename = Column(String(250), nullable=False)
    process_id = Column(Integer, nullable=False)
    title = Column(String(250,convert_unicode=True), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    process_type_id = Column(Integer, ForeignKey(ProcessType.id))
    process_type = relationship(ProcessType,backref='process')

    def __init__(self, filename, process_id, title, session, start_time,end_time):
        self.filename = filename
        self.process_id = process_id
        self.title = title.encode('string_escape')
        self.start_time = start_time
        self.end_time = end_time
        try:
            process_type = session.query(ProcessType) \
                .filter(ProcessType.filepath == filename, ProcessType.title == self.title).one()
        except InvalidRequestError:
            process_type = ProcessType(filepath=filename,title=self.title)
            session.add(process_type)
        self.process_type = process_type
        self.process_type_id = process_type.id
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



