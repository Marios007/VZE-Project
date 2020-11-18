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
        self.setFilePath("")
        image = None
        filePath, _ = QFileDialog.getOpenFileName(None, 'Open file',"C:\\", "Usable files (*.jpg *.jpeg *.gif *.png *.bmp *.avi *.mov *.mp4 *.mpeg)")
        
        if(filePath != ""):
    
            #Status 1 --> Bild, Status 2 --> Video, Status -1 --> Fehler
            status_type,imagepath = self.preprocessor.check_fileType(filePath)
            
            if(status_type == -1):
                return -1,"Der Dateityp ist leider nicht richtig",None

            print("File-Type-Check passed")

            #Status 1 --> Auflösung OK, Status -1 --> Auflösung zu hoch, Status -2 --> Auflösung zu niedrig
            status_res = self.preprocessor.check_fileResolution(status_type, filePath)

            if(status_res == -1):
                return -1,"Die Auflösung ist leider zu hoch",None
            if(status_res == -2):
                return -1,"Die Auflösung ist leider zu niedrig",None

            print("File-Resolution-Check passed")

            if(status_type == 2):
                #Status 1 --> Länge OK, Status -1 --> VIdeo zu lang
                status_len = self.preprocessor.check_fileLength(filePath)

                if(status_len == -1):
                    return -1,"Das Video ist leider zu lang",None
                
            print("File-Length-Check passed")

            self.setFilePath(filePath)
            return 0,"Datei erfolgreich ausgewählt",imagepath
            
            
        else:
            return -1,"Es wurde keine Datei ausgewählt",None

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