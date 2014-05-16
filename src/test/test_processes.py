import unittest
import os
import datetime
import time

import pst.processes
import pst.Process
import pst.screenshots
import pst.db
from pst.db import DBConnection
from pst.helpers import rm

class TestProcessFetcher(unittest.TestCase):
    def test_simple_fetch(self):
        currentProcess = pst.processes.get_current()
        self.assertTrue(type(currentProcess) is pst.Process.Process)
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
        for screenshot_path,screenshot_id in screenshots:
            self.assertTrue(os.path.exists(screenshot_path)
                and os.path.isfile(screenshot_path))
            self.assertTrue(type(screenshot_id) is int)
            rm(screenshot_path)

class TestDataBase(unittest.TestCase):
    def test_createdb(self):
        testdb = str(time.time())+".db"
        db = DBConnection(db_filename=testdb)
        self.assertTrue(os.path.exists(testdb)
            and os.path.isfile(testdb))
        db.session.close()
        rm(testdb)
    def test_save_process(self):
        # testdb = str(time.time())+".db"
        testdb ="test.db"
        currentProcess = pst.processes.get_current()
        db = DBConnection(db_filename=testdb)
        process = pst.db.Process(filename=currentProcess.filename,
                                 process_id=currentProcess.id,
                                 title=currentProcess.title,
                                 session=db.session)
        db.session.add(process)
        db.session.commit()
        self.assertTrue(type(process) is pst.db.Process)
        db.session.close()
    def test_save_screenshot(self):
        testdb = str(time.time())+".db"
        db = DBConnection(db_filename=testdb)
        screenshot_camera = pst.screenshots.Camera()
        screenshot_path, screenshot_id = screenshot_camera.take_screenshot(screenid=0)
        screenshot  = pst.db.Screenshot(screen_id=screenshot_id,
                                        file_path=screenshot_path,
                                        time_taken=datetime.datetime.now())
        db.session.add(screenshot)
        db.session.commit()
        self.assertTrue(type(screenshot) is pst.db.Screenshot)

        screenshot_from_db = db.session.query(pst.db.Screenshot)\
            .filter(pst.db.Screenshot.id == screenshot.id).one()
        self.assertTrue(type(screenshot_from_db) is pst.db.Screenshot)


        db.session.close()
        rm(testdb)
        rm(screenshot_path)
    def test_save_screenshots_all_screens(self):
        testdb = str(time.time())+".db"
        db = DBConnection(db_filename=testdb)
        screenshot_camera = pst.screenshots.Camera()
        screenshots = screenshot_camera.take_screenshot_all_displays()
        for screenshot_path,screenshot_id in screenshots:
            screenshot  = pst.db.Screenshot(screen_id=screenshot_id,
                                        file_path=screenshot_path,
                                        time_taken=datetime.datetime.now())
            db.session.add(screenshot)
            db.session.commit()
            self.assertTrue(type(screenshot) is pst.db.Screenshot)

            screenshot_from_db = db.session.query(pst.db.Screenshot)\
                .filter(pst.db.Screenshot.id == screenshot.id).one()
            self.assertTrue(type(screenshot_from_db) is pst.db.Screenshot)
        db.session.close()
        rm(testdb)
        rm(screenshot_path)



