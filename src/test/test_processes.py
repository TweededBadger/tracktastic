#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest
import os
import datetime
import time
import pst
import pst as Scheduler


import pst.Process
import pst.screenshots
import pst.db
from pst.db import DBConnection
from pst.helpers import rm,random_string

import pst.WebServer
from pst.DataService import DataService
from test import testhelpers


class TestProcessFetcher(unittest.TestCase):
    def test_simple_fetch(self):
        currentProcess = pst.processes.get_current()
        self.assertTrue(type(currentProcess) is pst.Process)
        self.assertTrue(type(currentProcess.filename) is unicode)
        self.assertTrue(type(currentProcess.id) is int)
        self.assertTrue(type(currentProcess.title) is str)


class TestScreenshot(unittest.TestCase):
    def test_takescreenshot(self):
        screenshot_camera = pst.screenshots.Camera()
        screenshot_path, screenshot_id = screenshot_camera.take_screenshot(screenid=0)
        self.assertTrue(os.path.exists(screenshot_path)
        and os.path.isfile(screenshot_path))
        self.assertTrue(type(screenshot_id) is int)
        rm(screenshot_path)

    def test_takescreenshot_all_screens(self):
        screenshot_camera = pst.screenshots.Camera()
        screenshots = screenshot_camera.take_screenshot_all_displays()
        for screenshot_path, screenshot_id in screenshots:
            self.assertTrue(os.path.exists(screenshot_path)
            and os.path.isfile(screenshot_path))
            self.assertTrue(type(screenshot_id) is int)
            rm(screenshot_path)


class TestDataBase(unittest.TestCase):
    def test_createdb(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        self.assertTrue(os.path.exists(testdb) and os.path.isfile(testdb))
        db.session.close()
        rm(testdb)

    def test_save_process(self):
        # testdb = str(time.time())+".db"
        testdb = "test.db"
        current_process = pst.processes.get_current()
        db = DBConnection(db_filename=testdb)
        process = db.add_process(current_process)
        self.assertTrue(type(process) is pst.db.DBProcess)
        db.session.close()

    def test_save_and_update_process(self):
        # testdb = str(time.time())+".db"
        testdb = "test.db"
        current_process = pst.processes.get_current()
        current_process.title = "TITLE: Unicode HOWTO � Python v2.7.7 documentation - Google Chrome"
        db = DBConnection(db_filename=testdb)
        process_start = db.add_process(current_process)
        time.sleep(0.5)
        second_current_process = pst.processes.get_current()
        process_end = db.add_process(current_process)
        process_end.title = "TITLE: Unicode HOWTO � Python v2.7.7 documentation - Google Chrome"
        self.assertEquals(process_start.id,process_end.id);
        self.assertNotEquals(process_end.start_time,process_end.end_time);
        db.session.close()
        # rm(testdb)
    def test_save_screenshot(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        screenshot_camera = pst.screenshots.Camera()
        screenshot_path, screenshot_id = screenshot_camera.take_screenshot(screenid=0)
        screenshot = db.add_screenshot(screenshot_id, screenshot_path)
        self.assertTrue(type(screenshot) is pst.db.Screenshot)

        screenshot_from_db = db.session.query(pst.db.Screenshot) \
            .filter(pst.db.Screenshot.id == screenshot.id).one()
        self.assertTrue(type(screenshot_from_db) is pst.db.Screenshot)

        db.session.close()
        rm(testdb)
        rm(screenshot_path)

    def test_save_screenshots_all_screens(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        screenshot_camera = pst.screenshots.Camera()
        screenshots = screenshot_camera.take_screenshot_all_displays()
        for screenshot_path, screenshot_id in screenshots:
            screenshot = db.add_screenshot(screenshot_id, screenshot_path)
            self.assertTrue(type(screenshot) is pst.db.Screenshot)

            screenshot_from_db = db.session.query(pst.db.Screenshot) \
                .filter(pst.db.Screenshot.id == screenshot.id).one()
            self.assertTrue(type(screenshot_from_db) is pst.db.Screenshot)
        db.session.close()
        rm(testdb)
        rm(screenshot_path)

    def test_get_screenshots_json(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        screenshot_camera = pst.screenshots.Camera()
        screenshots = screenshot_camera.take_screenshot_all_displays()
        for screenshot_path, screenshot_id in screenshots:
            screenshot = db.add_screenshot(screenshot_id, screenshot_path)
            self.assertTrue(type(screenshot) is pst.db.Screenshot)

        screenshots = [pst.db.row2dict(row) for row in db.get_screenshots()]
        print json.dumps(screenshots, indent=4, sort_keys=True)

        self.assertTrue(len(screenshots) > 0)

        db.session.close()
        rm(testdb)
        rm(screenshot_path)

    def test_default_process_category(self):
        testdb = str(time.time()) + ".db"
        # testdb = "test.db"
        db = DBConnection(db_filename=testdb)
        pc = db.session.query(pst.db.ProcessCategory).one()
        self.assertTrue(pc.id == 0)
        db.session.close()
        rm(testdb)


    def test_add_process_category(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        new_category = db.add_category(title="TITLE",title_search = "test",filename_search = "test")
        self.assertEquals(new_category.id,1)
        pc = db.session.query(pst.db.ProcessCategory).filter(pst.db.ProcessCategory.title == "TITLE").one()
        self.assertEquals(pc.id,1)
        db.session.close()
        rm(testdb)

    def test_add_process_and_process_category_and_assign(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        for x in xrange(0,5):
            current_process = pst.processes.get_current()
            random_title = random_string(10)
            random_filename = random_string(10)
            current_process.title = "TEST TITLE " + random_title
            current_process.filename = "TEST FILENAME " + random_filename
            process = db.add_process(current_process)
            new_category = db.add_category(title="TITLE",title_search = random_title,filename_search = random_filename)
            db.assign_categories()
            # processes = db.get_processes()
            processes = [pst.db.row2dict(row) for row in db.get_processes()]
            self.assertEqual(new_category.id,int(processes[x]['process_category']['id']))
        db.session.close()
        rm(testdb)




class TestScheduler(unittest.TestCase):
    def test_scheduler(self):
        global thread_run
        thread_run = False

        def test_func():
            print "hello"
            global thread_run
            thread_run = True

        test_sched = Scheduler.Scheduler(test_func(),
                                         cycleTime=datetime.timedelta(seconds=1))
        test_sched.thread.start()
        time.sleep(2)
        self.assertTrue(thread_run)

class TestDataService(unittest.TestCase):
    def test_get_screenshots(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        testhelpers.take_and_add_screenshots(db)

        dataservice = DataService(testdb)
        data = dataservice.screenshots()
        print data
        jsonobj = json.loads(data)
        self.assertTrue(len(jsonobj) > 0)
        db.session.close()

    def test_get_processes(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        testhelpers.add_process(db)
        dataservice = DataService(testdb)
        data = dataservice.processes()
        print data
        jsonobj = json.loads(data)
        self.assertTrue(len(jsonobj) > 0)
