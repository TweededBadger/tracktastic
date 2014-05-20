import json

import cherrypy
from pst import DBConnection
import pst


class DataService:
    def __init__(self):
        pass

    @cherrypy.expose
    def default(self, *args, **kwargs):
        pass

    @cherrypy.expose
    def screenshots(self, *args, **kwargs):
        db = DBConnection()
        screenshots = [pst.db.row2dict(row) for row in db.get_screenshots()]
        out = json.dumps(screenshots, indent=4, sort_keys=True)
        db.session.close()
        return out

    @cherrypy.expose
    def processes(self, *args, **kwargs):
        db = DBConnection()
        processes = [pst.db.row2dict(row) for row in db.get_processes()]
        out = json.dumps(processes, indent=4, sort_keys=True)
        db.session.close()
        return out
