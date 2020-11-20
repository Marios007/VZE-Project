from PyQt5.QtWidgets import QFileDialog
from gui.VzeGui import *
from preprocessor import *
import abc
import os

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
        """
        This method is used for loading a file into the software
        """
        print("loading file method")
        #reset filePath and image
        self.setFilePath("")
        imagepath = None

        #open FileExplorer to let the user choose his file
        filePath, _ = QFileDialog.getOpenFileName(None, 'Open file',"C:\\", "Usable files (*.jpg *.jpeg *.gif *.png *.bmp *.avi *.mov *.mp4 *.mpeg)")
        
        #if user selects a file
        if(filePath != ""):
    
            #check the type of the file
            #Status 1 --> image, Status 2 --> video, Status -1 --> error
            status_type,image = self.preprocessor.check_fileType(filePath)
            
            #If a wrong datatype is detected
            if(status_type == -1):
                return -1,"Der Dateityp ist leider nicht richtig",None

            print("File-Type-Check passed")

            #check the resolution of the file
            #Status 1 --> resolution OK, Status -1 --> resolution too high, Status -2 --> resolution too low
            status_res = self.preprocessor.check_fileResolution(status_type, filePath)

            #if the file has a wrong resolution
            if(status_res == -1):
                return -1,"Die Auflösung ist leider zu hoch",None
            if(status_res == -2):
                return -1,"Die Auflösung ist leider zu niedrig",None

            print("File-Resolution-Check passed")

            #if the file is a video, check the length
            if(status_type == 2):
                #Status 1 --> length OK, Status -1 --> video too long
                status_len = self.preprocessor.check_fileLength(filePath)

                #if the file is too long
                if(status_len == -1):
                    return -1,"Das Video ist leider zu lang",None
                
            print("File-Length-Check passed")

            #if every check is passed, call method to set filePath
            self.setFilePath(filePath)
            #return that everything is OK and the path to the previewImage
            return 0,"Datei erfolgreich ausgewählt",image
            
        #if user canceled the operation and didn´t select a file    
        else:
            return -1,"Es wurde keine Datei ausgewählt",None

    #Setter-method for filePath
    def setFilePath(self, filepath):
        self._fileName = filepath
        print(self._fileName)

    #Getter-method for filePath
    def getFilePath(self):
        return self._fileName

    def checkFilePath(self,filepath):
        status = os.path.exists(filepath)
        return status

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