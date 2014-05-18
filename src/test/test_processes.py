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
from pst.helpers import rm

import pst.WebServer


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

class TextWebserver(unittest.TestCase):
    def test_start_webserver(self):
        server = pst.WebServer()
