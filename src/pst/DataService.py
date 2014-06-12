import json

import cherrypy
from datetime import datetime
from pst import DBConnection
import pst


class DataService:
    def __init__(self,dbname='pst.db'):
        self.dbname = dbname
        pass

    @cherrypy.expose
    def default(self, *args, **kwargs):
        pass

    @cherrypy.expose
    def screenshots(self, *args, **kwargs):
        db = DBConnection(self.dbname)
        screenshots = [pst.db.row2dict(row) for row in db.get_screenshots()]
        out = json.dumps(screenshots, indent=4, sort_keys=True)
        db.session.close()
        return out

    @cherrypy.expose
    def processes(self, *args, **kwargs):
        db = DBConnection(self.dbname)
        start_time = datetime.strptime(cherrypy.request.params.get("start_time"), "%a, %d %b %Y %H:%M:%S %Z")
        end_time = datetime.strptime(cherrypy.request.params.get("end_time"), "%a, %d %b %Y %H:%M:%S %Z")
        print start_time
        print end_time
        processes = [pst.db.row2dict(row) for row in db.get_processes(start_time=start_time,end_time=end_time)]
        out = json.dumps(processes, indent=4, sort_keys=True)
        db.session.close()
        return out
