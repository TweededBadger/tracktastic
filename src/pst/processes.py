try:
    import win32gui
    import win32process
except:
    pass
from subprocess import Popen,PIPE
import re
import psutil
import pst
import sys


def get_current():
    if sys.platform.startswith("win"):
        return  get_current_windows()
    elif sys.platform.startswith("linux"):
        return get_window_linux()
    else:
        raise ImportError("my module doesn't support this system")


def get_window_linux():
    root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)

    for line in root.stdout:
        m = re.search('^_NET_ACTIVE_WINDOW.* ([\w]+)$', line)
        if m != None:
            id_ = m.group(1)
            # id_w = Popen(['xprop', '-id', id_, 'WM_NAME'], stdout=PIPE)
            id_w = Popen(['xprop', '-id', id_], stdout=PIPE)
            break

    if id_w != None:
        for line in id_w.stdout:
            match = re.match("WM_NAME\(\w+\) = \"(?P<name>.+)\"$", line)
            if match != None:
                process_name = match.group("name")
            file_match = re.match("_OB_APP_CLASS\(\w+\) = \"(?P<name>.+)\"$", line)
            if file_match != None:
                process_file = file_match.group("name")

        if (process_name and process_file):
            return pst.Process(process_id=0,title=process_name,filename=unicode(process_file))


    return "Active window not found"

def get_current_windows():
    n = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText (n)
    t,p = win32process.GetWindowThreadProcessId(n)
    ps_process = psutil.Process(p)
    filename = ps_process.name()
    current_process = pst.Process(process_id=p,title=title,filename=ps_process.exe())
    return current_process