import json

import cherrypy
from pst import DBConnection
import pst


class DataService:
    def __init__(self):
        self.db = DBConnection()

    @cherrypy.expose
    def default(self, *args, **kwargs):
        screenshots = [pst.db.row2dict(row) for row in self.db.get_screenshots()]
        out = json.dumps(screenshots, indent=4, sort_keys=True)
        return out
