from PyQt5.QtWidgets import QFileDialog
from gui.VzeGui import *
from preprocessor import *
import abc

#interface definition
class GuiInterface(abc.ABC):
    
    @abc.abstractmethod
    def doSomething(self):
        return

    def loadFile(self):
        return

    def setFilePath(self, filepath):
        return

    def getFilePath(self):
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
    preprocessor = imagesProcessing()
    _fileName = None

    def __init__(self, logic):
        self.logic = logic

    def doSomething(self):
       print("We are doing something")

    def loadFile(self):
        print("loading file method")
        filePath, _ = QFileDialog.getOpenFileName(None, 'Open file',"C:\\", "Usable files (*.jpg *.jpeg *.gif *.png *.bmp *.avi *.mov *.mp4 *.mpeg)")
        if filePath:
            #print(filePath)
            status = self.preprocessor.check_File(filePath)
            if status:
                self.setFilePath(filePath)
            
            #return self.fileName
            
    def setFilePath(self, filepath):
        self._fileName = filepath
        print(self._fileName)

    def getFilePath(self):
        return self._fileName

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