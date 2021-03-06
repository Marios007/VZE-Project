from PyQt5.QtWidgets import QFileDialog, QApplication
from gui.VzeGui import VzeGui
from ki.VzeKI import VzeImageProcessing
from constants import *
import os


# interface definition
class GuiInterface():

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

    def setResultArray(self, signID):
        return


class VzeController(GuiInterface):

    _fileName = None
    _compareResult = False
    array_dataInput = [[0 for x in range(TOTAL_NUMBER_SIGNS)] for y in range(DATA_ARRAY_COLUMN_COUNT)]
    preprocessor = None
    isPicture = False

    def __init__(self):
        self.preprocessor = VzeImageProcessing(self)
        self.isPicture = False

    def loadFile(self):
        """
        This method is used for loading a file into the software
        """
        self.setFilePath("")
        filePath, _ = QFileDialog.getOpenFileName(None, 'Open file', "C:\\", "Usable files (*.jpg *.jpeg *.gif *.png *.bmp *.avi *.mov *.mp4 *.mpeg)")

        # if user selects a file
        if filePath != "":
            # Status 1 --> image, Status 2 --> video, Status -1 --> error
            status_type, image = self.preprocessor.check_fileType(filePath)
            if status_type == 1:
                self.isPicture = True
            if status_type == 2:
                self.isPicture = False
            if status_type == -1:
                return -1, "Dieser Dateityp wird nicht unterstützt.\nUnterstütze Dateitypen: *.jpg *.jpeg *.gif *.png *.bmp *.avi *.mov *.mp4 *.mpeg", None
            print("File-Type-Check passed")

            # Status 1 --> resolution OK, 
            # Status -1 --> video resolution too high, 
            # Status -2 --> video resolution too low
            # Status -3 --> image resolution too high, 
            # Status -4 --> image resolution too low
            status_res = self.preprocessor.check_fileResolution(status_type, filePath)
            if status_res == -1:
                return -1, "Die Auflösung ist zu hoch. Die maximale Auflösung beträgt 1920x1080.", None
            elif status_res == -2:
                return -1, "Die Auflösung ist zu gering. Die Mindestauflösung beträgt 800x600.", None
            elif status_res == -3:
                return -1, "Die Auflösung ist zu hoch. Die maximale Auflösung beträgt 6000x4000.", None
            elif status_res == -4:
                return -1, "Die Auflösung ist zu gering. Die Mindestauflösung beträgt 800x600.", None

            print("File-Resolution-Check passed")
            if status_type == 2:
                # Status 1 --> length OK, Status -1 --> video too long
                status_len = self.preprocessor.check_fileLength(filePath)
                if status_len == -1:
                    return -1, "Das Video ist zu lang. Die maximale Videolänge beträgt 10 Minuten.", None

            print("File-Length-Check passed")
            self.setFilePath(filePath)
            return 0, "Datei erfolgreich ausgewählt", image
        else:
            return -2, "Es wurde keine Datei ausgewählt", None

    def setFilePath(self, filepath):
        self._fileName = filepath

    def getFilePath(self):
        return self._fileName

    def setCompareResult(self, compare):
        print("compareResult is set to " + str(compare))
        self._compareResult = compare

    def getCompareResult(self):
        return self._compareResult

    def setDataArray(self, signID, colID, val):
        self.array_dataInput[colID][signID] = val

    def getDataArray(self, signID, colID):
        return self.array_dataInput[colID][signID]

    def resetDataArray(self):
        self.array_dataInput = [[0 for x in range(TOTAL_NUMBER_SIGNS)] for y in range(DATA_ARRAY_COLUMN_COUNT)]

    def setResultArray(self, signID):
        val = self.getDataArray(signID, DATA_ARRAY_SIGN_DETECTED)
        self.setDataArray(signID, DATA_ARRAY_SIGN_DETECTED, val+1)
        return

    def checkFilePath(self, filepath):
        status = os.path.exists(filepath)
        return status

    def startAnalysis(self):
        # Method to start the analysis
        print("Method startAnalysis in VzeApp")

        sign_count = 0
        percentage_count = 0
        percentage_result = 0

        sign_id = ""
        sign_input = 0
        sign_detected = 0

        for array_count in range(len(self.array_dataInput[0])):
            sign_id = self.getDataArray(array_count, DATA_ARRAY_SIGN_ID)
            sign_input = int(self.getDataArray(array_count, DATA_ARRAY_SIGN_INPUT))
            sign_detected = int(self.getDataArray(array_count, DATA_ARRAY_SIGN_DETECTED))


            if sign_input == 0 and sign_detected == 0:
                percentage_count = percentage_count + 0
                #print("Sign " + sign_id + " is not relevant for analyzis")
            
            elif sign_input == sign_detected:
                percentage_count = percentage_count + 0
                sign_count = sign_count + sign_input
                print("Sign " + sign_id + " was detected correct")
                print("PercentageCount: " + str(percentage_count) + " SignCount: " + str(sign_count))

            elif sign_detected > sign_input:
                sum = sign_input - sign_detected
                diff = abs(sum / sign_detected)
                percentage = diff * 100
                percentage_mult = sign_detected * percentage
                percentage_count = percentage_count + percentage_mult
                sign_count = sign_count + sign_detected
                print("Sign " + sign_id + ": detected: " + str(sign_detected) + " input: " + str(sign_input))
                print("PercentageCount: " + str(percentage_count) + " SignCount: " + str(sign_count))

            else:
                sum = sign_detected - sign_input 
                diff = abs(sum / sign_input)
                percentage = diff * 100
                percentage_mult = sign_input * percentage
                percentage_count = percentage_count + percentage_mult
                sign_count = sign_count + sign_input
                print("Sign " + sign_id + ": detected: " + str(sign_detected) + " input: " + str(sign_input))
                print("PercentageCount: " + str(percentage_count) + " SignCount: " + str(sign_count))

        percentage_result = int(round(percentage_count / sign_count, 0))
        percentage_result = 100 - percentage_result
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
