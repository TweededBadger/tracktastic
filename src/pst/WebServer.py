import cherrypy.lib.auth_basic
import os

from configobj import ConfigObj
from pst.DataService import DataService

config = ConfigObj("config.ini")

class WebServer():
    def __init__(self,options={}):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        options.setdefault('port', 8081)
        options.setdefault('screenshots_dir', current_dir)
        options.setdefault('db', "pst.db")
        options_dict = {
            'server.socket_port': options['port'],
            'log.screen':True
        }
        cherrypy.config.update(options_dict)
        print current_dir
        print options['screenshots_dir']
        conf = {
            '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': current_dir+"/wwwroot",
                'tools.staticdir.index': 'index.html'
                # 'tools.staticdir.dir': "C:\\Work\\Personal\\Python\\TimeTracker\\src\\wwwroot\\",
            },
            '/screenshots' : {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': options['screenshots_dir']
            }
        }
        self.web_interface = WebInterface(db_file=options['db'])
        app = cherrypy.tree.mount(self.web_interface, '/', conf)
        cherrypy.server.start()
        cherrypy.server.wait()
    def close(self):
        cherrypy.engine.exit()


class WebInterface():
    def __init__(self,db_file):
        self.db_file = db_file
        self.data = DataService(dbname=self.db_file)
        pass
    @cherrypy.expose
    def index(self):
        pass





