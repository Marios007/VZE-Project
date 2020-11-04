from PyQt5.QtWidgets import QFileDialog
from gui.VzeGui import *


class GuiInterface:

    def doSomething(self):
        return

    def loadFile(self):
        return

    def processCV(self, filename):
        return


class openCV_Interface:

    def openCVMethod(self):
        return

    def loadFile1(self):
        return


class openCvController(openCV_Interface):

    logic = None

    def __init__(self):
        m_var = None

    def openCVMethod(self):
        print("openCVMethod")
        return

    def loadFile1(self):
        return


class VzeController(GuiInterface):

    logic = None
    opencv = openCvController()
    fileName = None

    def __init__(self, logic):
        self.logic = logic

    def doSomething(self):
        print("We are doing something")

    def loadFile(self):
        print("loading file method")
        self.fileName, _ = QFileDialog.getOpenFileName(None, 'Open file',"C:\\", "Image files(*.jpg *.svg *.png);;Video files(*.mp4)")
        if self.fileName:
            print(self.fileName)
            self.opencv.openCVMethod()
            
    def processCV(self):
        self.opencv.openCVMethod()

class VzeApp(QtWidgets.QApplication):

    mainWidget = None
    mainLogic = None
    
    def __init__(self, *args, **kwargs):
        super(VzeApp, self).__init__(*args,**kwargs)

        #init logic
        self.mainLogic = VzeController(self.mainLogic)

        #init gui
        self.mainWidget = VzeGui(self.mainLogic)

        #show gui
        self.mainWidget.show()