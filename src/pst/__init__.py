import datetime
import time

from configobj import ConfigObj

from .Schedluler import Scheduler
from .Process import Process
from .db import DBConnection
from .WebServer import WebServer
import processes
import screenshots

config = ConfigObj("config.ini")


class Main():
    def __init__(self):
        self.db = DBConnection()
        # self.schedule_camera = Scheduler(ScreenshotLoop(db=self.db),
        #                                  cycleTime=datetime.timedelta(seconds=10),threadName="CameraThread")
        # self.schedule_camera.thread.start()
        self.process_loop = Scheduler(ProccessLoop(db=self.db), cycleTime=datetime.timedelta(seconds=10),threadName="ProcessThread")
        self.process_loop.thread.start()

        self.start_webserver()

    def start_webserver(self):
        try:
            WEB_PORT = config['web_port']
        except:
            WEB_PORT = 8081

        try:
            SCREENSHOT_FOLDER = config['screenshot_folder']
        except:
            SCREENSHOT_FOLDER = "screenshots/"


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


class ProccessLoop():
    def __init__(self, db):
        self.db = DBConnection()

    def run(self):
        current_process = processes.get_current()
        print current_process.title
        self.db.add_process(current_process)


def main():
    main = Main()