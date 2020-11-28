from PyQt5.QtWidgets import QFileDialog, QApplication
from gui.VzeGui import VzeGui
from ki.VzeKI import VzeImageProcessing
import abc
import os


# interface definition
class GuiInterface(abc.ABC):

    def loadFile(self):
        return

    def setFilePath(self, filepath):
        return

    def getFilePath(self):
        return

    def checkFilePath(self, filepath):
        return

    def processCV(self):
        return

    def startVideo(self):
        return

    def startAnalysis(self):
        return


class VzeController(GuiInterface):

    _fileName = None
    _compareResult = False
    array_dataInput = [[0 for x in range(43)] for y in range(3)]
    preprocessor = None

    def __init__(self):
        self.preprocessor = VzeImageProcessing(self)

    def loadFile(self):
        """
        This method is used for loading a file into the software
        """
        self.setFilePath("")
        filePath, _ = QFileDialog.getOpenFileName(None, 'Open file', "C:\\", "Usable files (*.jpg *.jpeg *.gif *.png *.bmp *.avi *.mov *.mp4 *.mpeg)")

        # if user selects a file
        if filePath != "":
            # Status 1 --> image, Status 2 --> video, Status -1 --> error
            status_type,image = self.preprocessor.check_fileType(filePath)
            if status_type == -1 :
                return -1,"Dieser Dateityp wird nicht unterstützt.\nUnterstütze Dateitypen:\n*.jpg *.jpeg *.gif *.png *.bmp *.avi *.mov *.mp4 *.mpeg",None
            print("File-Type-Check passed")

            # Status 1 --> resolution OK, Status -1 --> resolution too high, Status -2 --> resolution too low
            status_res = self.preprocessor.check_fileResolution(status_type, filePath)
            if status_res == -1:
                return -1, "Die Auflösung ist zu hoch", None
            if status_res == -2 :
                return -1, "Die Auflösung ist zu gering", None

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

    def setCompareResult(self, compare):
        print("compareResult is set to " + str(compare))
        self._compareResult = compare

    def getCompareResult(self):
        return self._compareResult

    def checkFilePath(self, filepath):
        status = os.path.exists(filepath)
        return status

    def startAnalysis(self):
        # Method to start the analysis
        print("Method startAnalysis in VzeApp")

        percentage_result=0
        sign_id = ""
        sign_detected = 0
        sign_input = 0
        sign_count = 43
        percentage_counter = 0

        # Testausgabe des gesamten Arrays
        for array_count in range(len(self.array_dataInput[0])):
            percentage = 0
            sign_id = self.array_dataInput[0][array_count]
            sign_input = int(self.array_dataInput[1][array_count])
            sign_detected = int(self.array_dataInput[2][array_count])

            # percentage must only be calculated when customer expects the sign
            if(sign_input > 0):
                # Hier die Berechnung ausführen:
                # | (erkannte Schilder - eingegebene Schilder) / eingegebene Schilder | * 100
                sum = (sign_detected - sign_input)
                diff = abs(sum / sign_input)
                percentage = diff * 100
                percentage_counter = percentage_counter + percentage
                # print("SignId: " + str(sign_id) + "; Input: " + str(sign_input) + "; Detected: " + str(sign_detected) + "; Percentage: " + str(percentage))
            # print("Percentage Counter: " + str(percentage_counter))

        percentage_result = int(round(percentage_counter / 43, 0))
        # print("Percentage Result: " + str(percentage_result))
        return percentage_result


class VzeApp(QApplication):

    mainWidget = None
    mainLogic = None

    def __init__(self, *args, **kwargs):
        super(VzeApp, self).__init__(*args, **kwargs)

        # init logic
        self.mainLogic = VzeController()

        # init gui
        self.mainWidget = VzeGui(self.mainLogic)

        # show gui
        self.mainWidget.show()
