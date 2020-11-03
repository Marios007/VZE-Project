from PyQt5.QtWidgets import QFileDialog
from gui.VzeGui import *

class GuiInterface:

    def doSomething(self):
        return

    def loadFile(self):
        return

    def processCV(self):
        return

class openCV_Interface:

    def openCVMethod(self):
        return

    def loadFile1(self):
        return


class openCvController(openCV_Interface):

    logic = None

    def __init__(self, logic):
        self.logic = logic

    def openCVMethod(self):
        return

    def loadFile1(self):
        return

class VzeController(GuiInterface):

    logic = None
    opencv = openCV_Interface()

    def __init__(self, logic):
        self.logic = logic

    def doSomething(self):
        print("We are doing something")

    def loadFile(self):
        print("loading file method")
        fileName, _ = QFileDialog.getOpenFileName(None, 'Open file',"C:\\", "Image files(*.jpg *.svg *.png);;Video files(*.mp4)")
        if fileName:
            print(fileName)
            self.logic.openCVMethod()

    def processCV(self, filename):
        self.opencv.doSomething1()

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