import datetime
import win32gui
from pst import Scheduler
import pyHook,pythoncom
import threading,thread

class ActivityChecker():
    def __init__(self, timeout = 30):
        self.timeout = timeout
        self.active = True
        # thread.start_new_thread(self.startThread,())
        self.last_interaction = datetime.datetime.now()
        # self.thread = ActivityCheckerThread()
        # self.thread.start()
        # print self.thread.name
        self.loop = Scheduler(ActivityCheckLoop(),
                              cycleTime=datetime.timedelta(seconds=0.3),threadName="ActivityCheckerThread")
        self.loop.thread.start()
    def stop(self):

        # self.thread.running = False
        self.loop.abort = True
        pass
    def checkActive(self):
        time_since_interaction =  datetime.datetime.now() - self.loop.action.last_interaction
        if (time_since_interaction.total_seconds() > self.timeout):
            self.active = False
        else:
            self.active = True
        return self.active

class ActivityCheckLoop():
    def __init__(self):
        self.lastPos = None
        self.last_interaction = datetime.datetime.now()
    def run(self):
        flags, hcursor, newpos = win32gui.GetCursorInfo()
        if newpos != self.lastPos:
            self.lastPos = newpos
            self.last_interaction = datetime.datetime.now()

class ActivityCheckerThread(threading.Thread):
    def run(self):
        self.hm = pyHook.HookManager()
        self.hm.MouseAll = self.onMouseEvent
        self.hm.HookMouse()
        self.last_interaction = datetime.now()
        self.running = True
        while (self.running):
            pythoncom.PumpWaitingMessages()
    def onMouseEvent(self,event):
        # print 'MessageName:',event.MessageName
        # print 'Message:',event.Message
        # print 'Time:',event.Time
        # print 'Window:',event.Window
        # print 'WindowName:',event.WindowName
        # print 'Position:',event.Position
        # print 'Wheel:',event.Wheel
        # print 'Injected:',event.Injected
        # print '---'
        self.last_interaction = datetime.now()
        return True
