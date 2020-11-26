from PyQt5.QtWidgets import QFileDialog
from gui.VzeGui import *
from ki.VzeKI import *
import abc
import os

#interface definition
class GuiInterface(abc.ABC):
    
    def loadFile(self):
        return

    def setFilePath(self, filepath):
        return

    def getFilePath(self):
        return

    def checkFilePath(self,filepath):
        return

    def processCV(self):
        return

    def startVideo(self):
        return

    def startAnalysis(self):
        return

class openCV_Interface(abc.ABC):

    def openCVMethod(self):
        return

    def startVideo(self):
        return

    def streaming(self):
        return


class openCvController(openCV_Interface):
    
    logic = None

    def __init__(self, logic):
        self.logic = logic

    def openCVMethod(self):
        print("openCVMethod")
        return

    def startVideo(self):
        return

    def streaming(self, frame):
        return


class VzeController(GuiInterface):

    _fileName = None
    _compareResult = False
    preprocessor = None

    def __init__(self):
        self.preprocessor = VzeImageProcessing(openCvController, self)

    def loadFile(self):
        """
        This method is used for loading a file into the software
        """
        self.setFilePath("")
        filePath, _ = QFileDialog.getOpenFileName(None, 'Open file',"C:\\", "Usable files (*.jpg *.jpeg *.gif *.png *.bmp *.avi *.mov *.mp4 *.mpeg)")
        
        #if user selects a file
        if filePath != "":
            #Status 1 --> image, Status 2 --> video, Status -1 --> error
            status_type,image = self.preprocessor.check_fileType(filePath)
            if status_type == -1 :
                return -1,"Dieser Dateityp wird nicht unterstützt\nUnterstütze Dateitypen:\n*.jpg *.jpeg *.gif *.png *.bmp *.avi *.mov *.mp4 *.mpeg",None
            print("File-Type-Check passed")
            
            #Status 1 --> resolution OK, Status -1 --> resolution too high, Status -2 --> resolution too low
            status_res = self.preprocessor.check_fileResolution(status_type, filePath)
            if status_res == -1:
                return -1,"Die Auflösung ist zu hoch",None
            if status_res == -2 :
                return -1,"Die Auflösung ist zu gering",None

            print("File-Resolution-Check passed")
            if status_type == 2 :
                #Status 1 --> length OK, Status -1 --> video too long
                status_len = self.preprocessor.check_fileLength(filePath)
                if status_len == -1:
                    return -1,"Das Video ist leider zu lang",None
                
            print("File-Length-Check passed")
            self.setFilePath(filePath)
            return 0,"Datei erfolgreich ausgewählt",image
        else:
            return -2,"Es wurde keine Datei ausgewählt",None

    def setFilePath(self, filepath):
        self._fileName = filepath

    def getFilePath(self):
        return self._fileName

    def setCompareResult(self,compare):
        self._compareResult = compare

    def getCompareResult(self):
        return self._compareResult

    def checkFilePath(self,filepath):
        status = os.path.exists(filepath)
        return status

    def processCV(self):
        self.preprocessor.openCVMethod()

    def startAnalysis(self):
        #Method to start the analysis
        print("Method startAnalysis in VzeApp")  

class VzeApp(QtWidgets.QApplication):

    mainWidget = None
    mainLogic = None
    
    def __init__(self, *args, **kwargs):
        super(VzeApp, self).__init__(*args,**kwargs)

        #init logic
        self.mainLogic = VzeController()

        #init gui
        self.mainWidget = VzeGui(self.mainLogic)

        #show gui
        self.mainWidget.show()