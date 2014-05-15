import unittest
import os

import pst.processes
import pst.Process
import pst.screenshots



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
        screenshot_path = screenshot_camera.take_screenshot(screenid=0)
        self.assertTrue(os.path.exists(screenshot_path)
            and os.path.isfile(screenshot_path))
    def test_takescreenshot_all_screens(self):
        screenshot_camera = pst.screenshots.Camera()
        screenshot_paths = screenshot_camera.take_screenshot_all_displays()
        for screenshot_path in screenshot_paths:
            self.assertTrue(os.path.exists(screenshot_path)
            and os.path.isfile(screenshot_path))
