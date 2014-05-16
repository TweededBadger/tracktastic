import wx

class Camera(object):
    def __init__(self,save_path = ""):
        self.save_path = save_path
        self.app = wx.PySimpleApp()
        self.displays = [wx.Display(i) for i in range(wx.Display.GetCount())]

    def take_screenshot(self,screenid = 0,filename="screenshot",filetype=".jpg",display=None):
        if display is None:
            display = self.displays[screenid]
        geometry = display.GetGeometry()
        context = wx.ScreenDC()
        w,h = (geometry.Size)
        bitmap = wx.EmptyBitmap(w, h, -1)
        memory = wx.MemoryDC()
        memory.SelectObject(bitmap)
        memory.Blit(0, 0, w, h, context, geometry.Left, geometry.Top)
        memory.SelectObject(wx.NullBitmap)
        fullfilepath = self.save_path+filename+" - "+str(screenid)+filetype
        if (".jpg" in filetype):
            bitmap.SaveFile(fullfilepath, wx.BITMAP_TYPE_JPEG)
        #bitmap.SaveFile("screencapture.bmp", wx.BITMAP_TYPE_BMP)
        #bitmap.SaveFile("screencapture.jpg", wx.BITMAP_TYPE_JPEG)
        #bitmap.SaveFile("screencapture.png", wx.BITMAP_TYPE_PNG)

        return fullfilepath,screenid

    def take_screenshot_all_displays(self,filename="screenshot",filetype=".jpg"):
        screenshots = [ self.take_screenshot(screenid=index,filename=filename,filetype=filetype)
                  for index,display in enumerate(self.displays)]
        # for index,display in enumerate(self.displays):
        #     self.take_screenshot(screenid=index)
        #     ]
        return screenshots
