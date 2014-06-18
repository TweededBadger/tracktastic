import datetime
import time

from configobj import ConfigObj

from .Schedluler import Scheduler
from .Process import Process
from .db import DBConnection
from .WebServer import WebServer
import processes
from pst.ActivityChecker import ActivityChecker
import screenshots

config = ConfigObj("config.ini")


class Main():
    def __init__(self):
        self.db = DBConnection()
        # self.schedule_camera = Scheduler(ScreenshotLoop(db=self.db),
        #                                  cycleTime=datetime.timedelta(seconds=1),threadName="CameraThread")
        # self.schedule_camera.thread.start()
        self.process_loop = Scheduler(ProcessLoop(db=self.db), cycleTime=datetime.timedelta(seconds=1),threadName="ProcessThread")
        self.process_loop.thread.start()

        self.start_webserver()

    def start_webserver(self):
        try:
            WEB_PORT = config['web_port']
        except:
            WEB_PORT = 8081

        SCREENSHOT_FOLDER = config['screenshot_folder']

        self.server = WebServer({
            'port':WEB_PORT,
            'screenshots_dir':SCREENSHOT_FOLDER
        })


class ScreenshotLoop():
    def __init__(self, db):
        self.db = DBConnection()
        screenshot_folder = config['screenshot_folder']
        self.camera = screenshots.Camera(save_path=screenshot_folder)

    def run(self):
        screenshots = self.camera.take_screenshot_all_displays(filename=str(time.time()))
        for screenshot_path, screenshot_id in screenshots:
            screenshot = self.db.add_screenshot(screenshot_id, screenshot_path)


class ProcessLoop():
    def __init__(self, db):
        self.db = DBConnection()
        self.ac = ActivityChecker()
    def run(self):
        if (self.ac.checkActive()):
            current_process = processes.get_current()
            added_process = self.db.add_process(current_process)
        else:
            self.db.set_current_process_inactive()
        pass


def main():
    main = Main()