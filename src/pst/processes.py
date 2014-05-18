import win32gui
import win32process
import psutil
import pst


def get_current():
    n = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText (n)
    t,p = win32process.GetWindowThreadProcessId(n)
    ps_process = psutil.Process(p)
    filename = ps_process.name()
    current_process = pst.Process(process_id=p,title=title,filename=ps_process.exe())
    return current_process