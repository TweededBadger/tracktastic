
import json
import unittest
import urllib
from StringIO import StringIO
import cherrypy
import pst
from pst.helpers import random_string


def take_and_add_screenshots(db):
    screenshot_camera = pst.screenshots.Camera()
    screenshots = screenshot_camera.take_screenshot_all_displays()
    for screenshot_path, screenshot_id in screenshots:
        screenshot = db.add_screenshot(screenshot_id, screenshot_path)


def add_process(db):
    current_process = pst.processes.get_current()
    process = db.add_process(current_process)
    return process

def add_process_and_type(db):
    current_process = pst.processes.get_current()
    random_title = random_string(10)
    random_filename = random_string(10)
    current_process.title = "TEST TITLE " + random_title
    current_process.filename = "TEST FILENAME " + random_filename
    process = db.add_process(current_process)
    new_category = db.add_category(title="TITLE")
    new_filter = db.add_filter(title_search = random_title,
                               filename_search = random_filename,
                               category_id=new_category.id)
    db.assign_categories()


class BaseCherryPyTestCase(unittest.TestCase):
    # def __init__(self):
    #     self.local = None
    #     self.remote = None

    def webapp_request(self, path='/', method='GET', **kwargs):
        headers = [('Host', '127.0.0.1')]
        qs = fd = None

        if method in ['POST', 'PUT']:
            qs = urllib.urlencode(kwargs)
            headers.append(('content-type', 'application/x-www-form-urlencoded'))
            headers.append(('content-length', '%d' % len(qs)))
            print qs
            fd = StringIO(qs)
            qs = None
        elif kwargs:
            qs = urllib.urlencode(kwargs)

        # Get our application and run the request against it
        app = cherrypy.tree.apps['']
        # Let's fake the local and remote addresses
        # Let's also use a non-secure scheme: 'http'
        request, response = app.get_serving(self.local, self.remote, 'http', 'HTTP/1.1')
        try:
            response = request.run(method, path, qs, 'HTTP/1.1', headers, fd)
        finally:
            if fd:
                fd.close()
                fd = None

        if response.output_status.startswith('500'):
            print response.body
            raise AssertionError("Unexpected error")

        # collapse the response into a bytestring
        response.collapse_body()
        return response