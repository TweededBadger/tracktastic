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
                # 'tools.staticdir.dir': "C:\\Work\\Personal\\Python\\TimeTracker\\src\\wwwroot\\",
            },
            '/screenshots' : {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': options['screenshots_dir']
            }
        }
        app = cherrypy.tree.mount(WebInterface(), '/', conf)
        cherrypy.server.start()
        cherrypy.server.wait()


class WebInterface():
    def __init__(self):
        pass
    @cherrypy.expose
    def index(self):
        pass

    data = DataService()

