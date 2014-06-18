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
        try:
            start_time = datetime.strptime(cherrypy.request.params.get("start_time"), "%a, %d %b %Y %H:%M:%S %Z")
        except:
            start_time = 0
        try:
            end_time = datetime.strptime(cherrypy.request.params.get("end_time"), "%a, %d %b %Y %H:%M:%S %Z")
        except:
            end_time = datetime.now()
        try:
            pid = cherrypy.request.params.get("id")
        except:
            pid = False

        processes = [pst.db.row2dict(row) for row in db.get_processes(start_time=start_time,end_time=end_time,pid=pid)]
        out = json.dumps(processes, indent=4, sort_keys=True)
        db.session.close()
        return out

    @cherrypy.expose
    def process_categories(self, *args, **kwargs):
        db = DBConnection(self.dbname)
        if 'POST' in cherrypy.request.method:
            title = cherrypy.request.params.get("title")
            title_search = cherrypy.request.params.get("title_search")
            filename_search = cherrypy.request.params.get("filename_search")
            try:
                assign = cherrypy.request.params.get("assign")
            except:
                assign = False
            new_cat = db.add_category(title)
            new_filer = db.add_filter(title_search=title_search,
                                      filename_search=filename_search,
                                      category_id=new_cat.id)
            if assign:
                db.assign_categories()
            # out = json.dumps(pst.db.row2dict(new_cat), indent=4, sort_keys=True)
            # db.session.close()
            # return out
        if 'DELETE' in cherrypy.request.method:
            id = cherrypy.request.params.get("id")
            db.delete_category(id)
            try:
                assign = cherrypy.request.params.get("assign")
            except:
                assign = False
            if assign:
                db.assign_categories()

        process_categories = db.get_process_categories()
        data = [pst.db.row2dict(row) for row in process_categories]
        out = json.dumps(data, indent=4, sort_keys=True)
        db.session.close()
        return out

    @cherrypy.expose
    def category_filters(self, *args, **kwargs):
        db = DBConnection(self.dbname)
        if 'POST' in cherrypy.request.method:
            title_search = cherrypy.request.params.get("title_search")
            filename_search = cherrypy.request.params.get("filename_search")
            category_id = cherrypy.request.params.get("category_id")
            try:
                assign = cherrypy.request.params.get("assign")
            except:
                assign = False
            new_filter = db.add_filter(title_search=title_search,
                                      filename_search=filename_search,
                                      category_id=category_id)
            if assign:
                db.assign_categories()
        filters = db.get_category_filters()
        data = [pst.db.row2dict(row) for row in filters]
        out = json.dumps(data, indent=4, sort_keys=True)
        db.session.close()
        return out

    @cherrypy.expose
    def reorder_categories(self, *args, **kwargs):
        db = DBConnection(self.dbname)
        if 'POST' in cherrypy.request.method:
            jsondata = cherrypy.request.params.get("data")
            try:
                data = json.loads(jsondata)
            except:
                data = [json.loads(row) for row in jsondata]
            edited_data = db.edit_categories(data)
            edited_data_dict =[pst.db.row2dict(row) for row in edited_data]
            out = json.dumps(edited_data_dict, indent=4, sort_keys=True)

            try:
                assign = cherrypy.request.params.get("assign")
            except:
                assign = False
            if assign:
                db.assign_categories()

            db.session.close()
            return out
        db.session.close()







