#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest
import os
import datetime
import time
import cherrypy
import pst
import pst as Scheduler
from pst.ActivityChecker import ActivityChecker

import pst.Process
import pst.screenshots
import pst.db
from pst.db import DBConnection
from pst.helpers import rm,random_string

import pst.WebServer
from pst.DataService import DataService
from test import testhelpers
from test.testhelpers import BaseCherryPyTestCase


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
        self.assertEqual(pc.process_filter[0].title_search,'')
        self.assertEqual(pc.process_filter[0].filename_search,'')
        db.session.close()
        rm(testdb)


    def test_add_process_category(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        new_category = db.add_category(title="TITLE")
        self.assertEquals(new_category.id,1)
        pc = db.session.query(pst.db.ProcessCategory).filter(pst.db.ProcessCategory.title == "TITLE").one()
        self.assertEquals(pc.id,1)
        db.session.close()
        rm(testdb)

    def test_add_process_and_process_category_and_assign(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        for x in xrange(0,10):
        # x = 0
            current_process = pst.processes.get_current()
            random_title = random_string(10)
            random_filename = random_string(10)
            current_process.title = "TEST TITLE " + random_title
            current_process.filename = "TEST FILENAME " + random_filename
            process = db.add_process(current_process)
            new_category = db.add_category(title="TITLE")
            new_filter = db.add_filter(category_id=new_category.id,title_search = random_title,filename_search = random_filename)
            db.assign_categories()
            # processes = db.get_processes()
            processes = [pst.db.row2dict(row) for row in db.get_processes()]
            self.assertEqual(new_category.id,int(processes[x]['process_categories'][0]['id']))
            self.assertEqual(new_filter.title_search,processes[x]['process_categories'][0]['filters'][0]['title_search'])
            self.assertEqual(new_filter.filename_search,processes[x]['process_categories'][0]['filters'][0]['filename_search'])
        db.session.close()
        rm(testdb)

    def test_add_process_category_filter(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)

        random_title = random_string(10)
        random_filename = random_string(10)
        new_category = db.add_category(title="TITLE")
        new_filter = db.add_filter(category_id=new_category.id,title_search = random_title,filename_search = random_filename)

        pc = db.session.query(pst.db.ProcessCategory).filter(pst.db.ProcessCategory.title == "TITLE").one()
        self.assertEquals(pc.id,1)
        self.assertEqual(pc.process_filter[0].title_search,random_title)
        self.assertEqual(pc.process_filter[0].filename_search,random_filename)
        db.session.close()
        rm(testdb)


    def test_inactive_then_active_process(self):
        testdb = str(time.time()) + ".db"
        db = DBConnection(db_filename=testdb)
        current_process = pst.processes.get_current()
        db.add_process(current_process)
        time.sleep(0.1)
        db.set_current_process_inactive()
        time.sleep(0.1)
        db.add_process(current_process)
        time.sleep(0.1)
        db.set_current_process_inactive()

        processes = [pst.db.row2dict(row) for row in db.get_processes()]
        self.assertEqual(len(processes),2)
        self.assertGreater(processes[0]['end_time'],processes[0]['start_time'])
        self.assertGreater(processes[1]['end_time'],processes[1]['start_time'])
        self.assertGreater(processes[1]['start_time'],processes[0]['end_time'])

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
    def setUp(self):
        self.testdb = str(time.time()) + ".db"
        self.db = DBConnection(db_filename=self.testdb)
        self.dataservice = DataService(self.testdb)
    def test_get_screenshots(self):
        testhelpers.take_and_add_screenshots(self.db)
        data = self.dataservice.screenshots()
        # print data
        jsonobj = json.loads(data)
        self.assertTrue(len(jsonobj) > 0)
    def test_get_processes(self):
        testhelpers.add_process(self.db)
        data = self.dataservice.processes()
        # print data
        jsonobj = json.loads(data)
        self.assertTrue(len(jsonobj) > 0)
    def test_get_process_cats(self):
        testhelpers.add_process_and_type(self.db)
        process_data = self.dataservice.processes()
        process_type_data = self.dataservice.process_categories()
        print process_type_data
        jsonobj = json.loads(process_type_data)
        self.assertTrue(len(jsonobj) > 0)
    def tearDown(self):
        self.db.session.close()
        rm(self.testdb)




class TestWebService(BaseCherryPyTestCase):

    def setUp(self):

        self.testdb = str(time.time()) + ".db"
        self.db = DBConnection(db_filename=self.testdb)
        # testhelpers.add_process_and_type(self.db)

        WEB_PORT = 8076
        self.local = cherrypy.lib.httputil.Host('127.0.0.1', 50000, "")
        self.remote  = cherrypy.lib.httputil.Host('127.0.0.1', WEB_PORT, "")
        SCREENSHOT_FOLDER = "testscreenshots/"
        self.server = pst.WebServer({
            'port':WEB_PORT,
            'screenshots_dir':SCREENSHOT_FOLDER,
            'db':self.testdb
        })

    def test_get_process_categories(self):
        response = self.webapp_request('/data/process_categories')
        self.assertEqual(response.output_status, '200 OK')
        # response body is wrapped into a list internally by CherryPy
        jsonobj = json.loads('\n\r'.join(response.body))
        print jsonobj
        self.assertTrue(len(jsonobj) > 0)
        # self.assertEqual(response.body, ['hello world'])

    def test_create_process_category(self):
        test_title = random_string(10)
        test_title_search = random_string(10)
        test_filename_search = random_string(10)
        current_process = pst.processes.get_current()
        current_process.title = "TEST TITLE " + test_title_search
        current_process.filename = "TEST FILENAME " + test_filename_search
        process = self.db.add_process(current_process)
        response = self.webapp_request('/data/process_categories',
                                      method='POST',
                                      title=test_title,
                                      title_search= test_title_search,
                                      filename_search=test_filename_search,
                                      assign=True)
        jsonobj = json.loads('\n\r'.join(response.body))
        new_cat = [x for x in jsonobj if x['title'] == test_title][0]
        self.assertEqual(new_cat['title'],test_title)
        self.assertEqual(new_cat['filters'][0]['title_search'],test_title_search)
        self.assertEqual(new_cat['filters'][0]['filename_search'],test_filename_search)

        process_responce = self.webapp_request('/data/processes',id=process.id)
        process_jsonobj = json.loads('\n\r'.join(process_responce.body))
        self.assertEqual(new_cat['id'],process_jsonobj[0]['process_categories'][0]['id'])

    def test_add_process_category_filter(self):
        test_title = random_string(10)
        test_title_search = random_string(10)
        test_filename_search = random_string(10)
        current_process = pst.processes.get_current()
        current_process.title = "TEST TITLE " + test_title_search
        current_process.filename = "TEST FILENAME " + test_filename_search
        process = self.db.add_process(current_process)
        response = self.webapp_request('/data/process_categories',
                                      method='POST',
                                      title=test_title,
                                      title_search= test_title_search,
                                      filename_search=test_filename_search,
                                      assign=True)
        jsonobj = json.loads('\n\r'.join(response.body))
        new_cat = [x for x in jsonobj if x['title'] == test_title][0]
        self.assertEqual(new_cat['title'],test_title)
        self.assertEqual(new_cat['filters'][0]['title_search'],test_title_search)
        self.assertEqual(new_cat['filters'][0]['filename_search'],test_filename_search)

        test_title_search2 = random_string(10)
        test_filename_search2 = random_string(10)

        response2 = self.webapp_request('/data/category_filters',
                                       method='POST',
                                       title_search= test_title_search2,
                                        filename_search=test_filename_search2,
                                        category_id= new_cat['id'],
                                        assign=True
                                       )
        jsonobj2 = json.loads('\n\r'.join(response2.body))


        response3 = self.webapp_request('/data/process_categories')
        jsonobj3 = json.loads('\n\r'.join(response3.body))
        new_cat2 = [x for x in jsonobj3 if x['title'] == test_title][0]
        self.assertGreater(len(new_cat2['filters']),1)
        self.assertEqual(new_cat2['filters'][1]['title_search'],test_title_search2)
        self.assertEqual(new_cat2['filters'][1]['filename_search'],test_filename_search2)



    def test_delete_process_category(self):
        test_title = random_string(10)
        test_title_search = random_string(10)
        test_filename_search = random_string(10)
        response = self.webapp_request('/data/process_categories',
                                      method='POST',
                                      title=test_title,
                                      title_search= test_title_search,
                                      filename_search=test_filename_search,
                                      assign=True)
        jsonobj = json.loads('\n\r'.join(response.body))
        new_cat = [x for x in jsonobj if x['title'] == test_title][0]
        self.assertEqual(new_cat['title'],test_title)
        self.assertEqual(new_cat['filters'][0]['title_search'],test_title_search)
        self.assertEqual(new_cat['filters'][0]['filename_search'],test_filename_search)

        response2 = self.webapp_request('/data/process_categories',
                                      method='DELETE',
                                      id=new_cat['id'],
                                      assign=True)
        jsonobj2 = json.loads('\n\r'.join(response2.body))
        print jsonobj2
        self.assertEqual(len(jsonobj2),1)
        self.assertEqual(len([x for x in jsonobj2 if x['title'] == test_title]),0)



    def test_reorder(self):
        new_cat_1 = self.db.add_category(title="TITLE1")
        new_cat_2 = self.db.add_category(title="TITLE2")
        new_cat_1_filter = self.db.add_filter(new_cat_1.id)
        new_cat_2_filter = self.db.add_filter(new_cat_2.id)
        cats = [pst.db.row2dict(row) for row in self.db.get_process_categories()]
        self.assertGreater(len(cats),2)
        for cat in cats:
            if cat['title'] == "TITLE2":
                cat['order'] = 1
            if cat['title'] == "TITLE1":
                cat['order'] = 2
        test_json = json.dumps(cats, indent=4, sort_keys=True)
        response = self.webapp_request('/data/reorder_categories',
                                      method='POST',
                                      data=test_json)

        jsonobj = json.loads('\n\r'.join(response.body))
        new_cat_1_amended_from_json = [x for x in jsonobj if x['title'] == "TITLE1"][0]
        new_cat_2_amended_from_json = [x for x in jsonobj if x['title'] == "TITLE2"][0]
        self.assertEqual(int(new_cat_1_amended_from_json['order']),2)
        self.assertEqual(int(new_cat_2_amended_from_json['order']),1)

        self.db.session.close()
        self.db = DBConnection(db_filename=self.testdb)

        cats2 = [pst.db.row2dict(row) for row in self.db.get_process_categories()]
        new_cat_1_amended = [x for x in cats2 if x['title'] == "TITLE1"][0]
        new_cat_2_amended = [x for x in cats2 if x['title'] == "TITLE2"][0]
        self.assertEqual(int(new_cat_1_amended['order']),2)
        self.assertEqual(int(new_cat_2_amended['order']),1)



    def tearDown(self):
        self.server.close()
        self.db.session.close()
        rm(self.testdb)


class TestActivityCheckerMouse(unittest.TestCase):
    def setUp(self):
        self.ac = ActivityChecker()
    def test_activity_checker_creation(self):
        time.sleep(0.5)
        self.assertTrue(self.ac.active)
    def test_no_activity(self):
        self.ac.timeout = 1
        print "Don't move the mouse"
        time.sleep(2)
        self.assertFalse(self.ac.checkActive())
    def test_activity(self):
        self.ac.timeout = 1
        print "Move the mouse"
        time.sleep(2)
        self.assertTrue(self.ac.checkActive())
    def tearDown(self):
        self.ac.stop()
        time.sleep(0.5)








