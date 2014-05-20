import json
import pst


def take_and_add_screenshots(db):
    screenshot_camera = pst.screenshots.Camera()
    screenshots = screenshot_camera.take_screenshot_all_displays()
    for screenshot_path, screenshot_id in screenshots:
        screenshot = db.add_screenshot(screenshot_id, screenshot_path)


def add_process(db):
    current_process = pst.processes.get_current()
    process = db.add_process(current_process)