from datetime import datetime
import pyHook,pythoncom
import threading,thread

class ActivityChecker():
    def __init__(self, timeout = 30):
        self.timeout = timeout
        self.active = True
        # thread.start_new_thread(self.startThread,())
        self.last_interaction = datetime.now()
        self.thread = ActivityCheckerThread()
        self.thread.start()
        print self.thread.name
    def stop(self):
        self.thread.running = False
    def checkActive(self):
        time_since_interaction =  datetime.now() - self.thread.last_interaction
        if (time_since_interaction.total_seconds() > self.timeout):
            self.active = False
        else:
            self.active = True
        return self.active

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
