from PyQt5 import QtCore, QtGui, QtWidgets
import gui.styles as styles
import gui.image_ressources as image_ressources
import constants as constants
from ki.VzeKI import VideoThread
from ki.VzeKI import VideoThreadKI
import csv
from collections import deque
from gui.RingBuffer import RingBuffer
import numpy as np


class MyMessageBox(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        #self.setSizeGripEnabled(False)

    def event(self, e):
        result = QtWidgets.QMessageBox.event(self, e)
        self.setFixedSize(constants.POPUP_MESSAGE_WIDHT, constants.POPUP_MESSAGE_HEIGHT)
        return result

class VzeGui(QtWidgets.QMainWindow):

    stack_lastScreen = []
    demo_video1 = "./gui/pics/DemoVideos/DemoVideo_gutesWetter.mp4"
    demo_video2 = "./gui/pics/DemoVideos/DemoVideo_schlechtesWetter.mp4"
    demo_datafile1 = "./gui/demo_data_1.csv"
    demo_datafile2 = "./gui/demo_data_2.csv"

    WIDTH_MIN = 0
    WIDTH_MAX = 960
    COUNT_BORDER_LEFT = 0.47
    COUNT_BORDER_RIGHT = 0.53
    COUNT_THRESHOLD = 10
    NEW_SIGN_BOUNDARIES = 150

    def __init__(self, logicInterface):
        QtWidgets.QMainWindow.__init__(self)
        print("loading UI")

        self.logic = logicInterface
        # ringbuffer to store 3 last detected shields
        self.ringBuffer = RingBuffer(3)
        # dict for counting shields
        self.dict = {}

        self.countArrLeft = np.empty((0,4), float)
        self.countArrRight = np.empty((0,4), float)

        # Setting Window Title and Icon
        self.setWindowTitle("VerkehrsZeichenErkennung VZE")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/logo_schild"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # Size of window is always 0,65 times of availabe window
        self.size = QtWidgets.QDesktopWidget().availableGeometry()
        self.setMinimumSize(self.size.width() * constants.WINDOW_SIZE_RATIO, self.size.height() * constants.WINDOW_SIZE_RATIO)

        # Main widget
        window = QtWidgets.QWidget()
        window.setStyleSheet(styles.styleBackground)
        self.setCentralWidget(window)
        window.setObjectName("window")

        # Set vertical layout for main window
        self.verticalLayout = QtWidgets.QVBoxLayout(window)
        self.verticalLayout.setObjectName("verticalLayout")

        # Set stacked widget
        self.stackedWidget = QtWidgets.QStackedWidget(window)
        self.stackedWidget.setStyleSheet(styles.styleBackground)
        self.stackedWidget.setObjectName("stackedWidget")

        self.build_screens()
        # define startscreen
        self.stackedWidget.setCurrentIndex(constants.START_SCREEN)
        QtCore.QMetaObject.connectSlotsByName(window)

        

    def build_screens(self):

        # Build UI with each screen
        print("Build screens")
        # 0
        self.startscreen = Ui_startscreen(self.logic, self)
        self.stackedWidget.addWidget(self.startscreen)
        # Screen ID 1
        self.demoscreen = Ui_demoscreen(self.logic, self)
        self.stackedWidget.addWidget(self.demoscreen)
        # Screen ID 2
        self.previewscreen = Ui_previewscreen(self.logic, self)
        self.stackedWidget.addWidget(self.previewscreen)
        # Screen ID 3
        self.diScreen = Ui_DIScreen(self.logic, self)
        self.stackedWidget.addWidget(self.diScreen)
        # Screen ID 4
        self.analyzepvscreen = Ui_analyzePvScreen(self.logic, self)
        self.stackedWidget.addWidget(self.analyzepvscreen)
        # Screen ID 5
        self.analyzescreen = Ui_analyzeScreen(self.logic, self)
        self.stackedWidget.addWidget(self.analyzescreen)
        # Screen ID 6
        self.demodatascreen = Ui_DemoDataScreen(self.logic, self)
        self.stackedWidget.addWidget(self.demodatascreen)
        # Screen ID 7
        self.resultscreen = Ui_ResultScreen(self.logic, self)
        self.stackedWidget.addWidget(self.resultscreen)
        # Screen ID 8
        self.infoscreen = Ui_InfoScreen(self.logic, self)

        self.verticalLayout.addWidget(self.stackedWidget)

    def change_screen(self, nextScreen):
        """
        change to next screen and save last screen to stack. When jump to screen 0 then initialize the stack
        """
        if nextScreen == constants.START_SCREEN:
            self.stackedWidget.setCurrentIndex(nextScreen)
            self.stack_lastScreen = []
        elif nextScreen != constants.START_SCREEN:
            self.set_lastScreen()
            self.stackedWidget.setCurrentIndex(nextScreen)
        return

    def set_lastScreen(self):
        """
        save the screen you are currently on onto a stack
        """
        self.stack_lastScreen.append(self.stackedWidget.currentIndex())
        # print("Save last screen: " + str(self.stackedWidget.currentIndex()))

    def change_screen_back(self):
        """
        go back to last screen and pop off last element from stack
        """
        # print("print stack: " + str(self.stack_lastScreen))
        self.stackedWidget.setCurrentIndex(self.stack_lastScreen.pop())
        return

    def create_DemoDataGrid(self, demoID):
        """
        creating the dataGrid for displaying the demoData
        """
        print("loading demo data grid for demovideo " + str(demoID))

        # set demodatafile according to the passed demoID
        demodatafile = ""
        if demoID == constants.DEMO_ID_1:
            demodatafile = self.demo_datafile1
        elif demoID == constants.DEMO_ID_2:
            demodatafile = self.demo_datafile2
        else:
            print("Unknown error")

        self.demodatascreen.delete_grid()
        self.demodatascreen.create_grid(demodatafile)
        self.change_screen(constants.DEMO_DATA_SCREEN)

    def createPixmap(self, numpy):
        """
        This method is used for creating a graphicsScene from an image file
        """
        image = QtGui.QImage(numpy, numpy.shape[1], numpy.shape[0], numpy.shape[1] * 3, QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(image)
        pixmap_scaled = pixmap.scaled(constants.PREVIEWIMAGE_WIDTH, constants.PREVIEWIMAGE_HEIGTH)
        return pixmap_scaled

    def showPreviewImage(self, numpy):
        """
        This method is used for displaying a previewImage on every previewScreen and the analyseScreen
        """
        # print("method showPreviewImage")
        pixmap = self.createPixmap(numpy)
        self.previewscreen.imageLayout.setPixmap(pixmap)
        self.analyzepvscreen.imageLayout.setPixmap(pixmap)
        self.analyzescreen.videoLayout.setPixmap(pixmap)


    def loadFile(self):
        """
        This method is used for uploading a file
        """
        status, message, image = self.logic.loadFile()
        if status == 0:
            self.showPreviewImage(image)
            self.change_screen(constants.PREVIEW_SCREEN)
        elif status == -1:
            print(message)
            title = "Fehler beim Laden der Datei"
            self.showPopup(title, message)
        else:
            print(message)

    def loadDemoVideo(self, filepath, demoID):
        """
        This method is used for loading one of the demo-videos, check if it exists,
        show its first image on the screens and go to the preview-screen
        """
        fileExists = self.logic.checkFilePath(filepath)
        if fileExists:
            image = self.logic.preprocessor.get_firstImage(filepath)
            self.logic.setFilePath(filepath)
            self.showPreviewImage(image)
            demodatafile = ""
            if demoID == constants.DEMO_ID_1:
                demodatafile=self.demo_datafile1
            elif demoID == constants.DEMO_ID_2:
                demodatafile=self.demo_datafile2
            self.loadDemoData(demodatafile)
            self.logic.setCompareResult(True)
            self.change_screen(constants.ANALYZE_PV_SCREEN)
        else:
            errorMessage = "Das Demovideo existiert nicht!\nBitte kontaktieren Sie den Support."
            errorTitle = "Fehler Demovideo"
            print("The given demoVideo does not exist: " + filepath)
            self.showPopup(errorTitle, errorMessage)
            self.change_screen(constants.START_SCREEN)

    def showPopup(self, title, message):
        """
        method for showing a popup with a title and a message (with Warning Icon)
        """
        print("popup method")
        self.popMsg = MyMessageBox()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/logo_schild"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.popMsg.setWindowIcon(icon)
        self.popMsg.setWindowTitle(title)
        self.popMsg.setText(message)
        self.popMsg.setIcon(QtWidgets.QMessageBox.Warning)
        self.popMsg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.popMsg.exec_()

    def cancel_Analyze(self):
        """
        method to cancel the Analysis of the current file and get back to the startscreen
        """
        # SL: Hier dann der Cancel der Analyse. Eventuell eine globale Variable mit True belegen, wenn die Analyse laufen soll
        # und dann beim Klicken des Abbrechen-Button auf False setzen.
        # In der Methode zum Video abspielen müsste dann nur in jedem Schleifendurchlauf diese abgefragt werden.
        self.cleanup()
        self.thread.stopVideo()
        self.change_screen(constants.START_SCREEN)

    def show_Result(self):
        """
        method where the analysis is started and the gridContent of the resultscreen is filled
        """
        self.resultscreen.set_ResultLabel()
        self.resultscreen.create_gridContent()
        self.change_screen(constants.RESULT_SCREEN)

    def loadDemoData(self, filepath):
        """
        method to load the demodatafile into the resultarray
        """
        with open(filepath, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')

            next(csv_reader)

            array_count = 0
            for line in csv_reader:
                self.sign_id = line[constants.DEMODATA_CSV_SIGN_ID]
                self.sign_count = int(line[constants.DEMODATA_CSV_SIGN_COUNT])

                self.logic.setDataArray(array_count, constants.DATA_ARRAY_SIGN_ID, self.sign_id)
                self.logic.setDataArray(array_count, constants.DATA_ARRAY_SIGN_INPUT, self.sign_count)
                self.logic.setDataArray(array_count, constants.DATA_ARRAY_SIGN_DETECTED, 0)

                array_count = array_count+1

        csvfile.close()

        print("Demo-Data loaded")
        # Testausgabe des gesamten Arrays
        # for j in range(len(self.logic.array_dataInput[constants.DATA_ARRAY_SIGN_ID])):
        #     print(self.logic.getDataArray(j, constants.DATA_ARRAY_SIGN_ID), end=' ')
        #     print(self.logic.getDataArray(j, constants.DATA_ARRAY_SIGN_INPUT), end=' ')
        #     print(self.logic.getDataArray(j, constants.DATA_ARRAY_SIGN_DETECTED), end=' ')
        #     print()

    def cleanup(self):
        """
        method for clearing all variables
        """
        print("CleanUp-Method")
        self.logic.resetDataArray()
        self.logic.setCompareResult(False)
        self.logic.setFilePath("")
        self.analyzescreen.deleteSignLabel()
        self.demodatascreen.delete_grid()
        self.diScreen.reset_gridContent()
        self.resultscreen.delete_grid()
        self.deactivateResultBtn()
        self.initRingBuffer()
        self.dict = {}
        self.change_screen(constants.START_SCREEN)

    def processKIData(self, inputObject):
        """
        Method is receiving the frame and all data from the AI and process it
        inputObject is a VzeKIObject
        """
        self.img = inputObject.frame
        # show the frame on the GUI
        self.setVideoImage(self.img)

        self.id = inputObject.frameId
        self.numDetectSigns = inputObject.numDetectSigns
        self.detectedSigns = inputObject.detectedSigns
        print("frameID:{0} - numDetectedSigns:{1}".format(self.id, self.numDetectSigns))
        
        if not self.logic.isPicture:
            self.countSigns(self.detectedSigns, self.numDetectSigns)
        else:
            self.countSignsInPic(self.detectedSigns, self.numDetectSigns)

    def countSigns(self, signArray, numDetectSigns): 
        for i in range(numDetectSigns):
            signObj = signArray[i]
            
            """
            if signObj.prob >= 96.:
                print("SignProb:" + str(signObj.prob))
                if signObj.signID in self.dict:
                    if self.dict[signObj.signID]==10:
                        self.logic.setResultArray(signObj.signID)
                        self.setSideLabels(signObj.signID)
                        self.dict[signObj.signID] = self.dict[signObj.signID]+1
                    else:
                        print("+1 in dict for id " +  str(signObj.signID))
                        self.dict[signObj.signID] = self.dict[signObj.signID]+1
                else:
                    print("add to dict" +  str(signObj.signID))
                    self.dict.update({signObj.signID : 1})
            print(self.dict)
            print("frameID:frame:{0} - signID:{1} - prob:{2} - box_W_H:{3} - ccordXY:{4}".format(self.id, signObj.signID, signObj.prob, signObj.box_W_H, signObj.coordinateXY ))
            """
            
            if signObj.prob >= 96.:
                _, y = signObj.coordinateXY
                if y >= self.COUNT_BORDER_RIGHT*self.WIDTH_MAX and y<= self.WIDTH_MAX:
                    self.countArrRight = self.fillArrayCount(self.countArrRight, signObj, y)
                    #print("RIGHT", self.countArrRight)
                if y < self.COUNT_BORDER_LEFT*self.WIDTH_MAX and y>= self.WIDTH_MIN:
                    self.countArrLeft = self.fillArrayCount(self.countArrLeft, signObj, y)
                    #print("LEFT", self.countArrLeft)

        return

    def fillArrayCount(self, countArray, signObj, y):
        # [:,0] == signIDs and [:,3] == count of each numpy array row
        if np.any(countArray[:,0] == signObj.signID):
            id_index = np.where(countArray[:,0] == signObj.signID)
            if countArray[id_index,2] <= y-self.NEW_SIGN_BOUNDARIES or countArray[id_index,2] >= y+self.NEW_SIGN_BOUNDARIES:
                countArray[id_index,3] = 0
                print()
                print("NEW SIGN", countArray[id_index,2], y, "ID", countArray[id_index,0])
                print()
            if countArray[id_index,3] == self.COUNT_THRESHOLD:
                    self.logic.setResultArray(signObj.signID)
                    self.setSideLabels(signObj.signID)
            countArray[id_index,3] += 1
            countArray[id_index,2] = y
        else: 
            # signID, signProbability, sign ymin, count
            countArray = np.vstack((countArray, np.array([signObj.signID, signObj.prob, y, 1])))
        return countArray


    def countSignsInPic(self, signArray, numDetectSigns): 
         for i in range(numDetectSigns):
            signObj = signArray[i]

            if signObj.prob >= 93.:
                self.setSideLabels(signObj.signID)
                self.logic.setResultArray(signObj.signID)


    def setSideLabels(self, detetedSign):
        detetedSignID = ":/signs/" + str(detetedSign)
        self.ringBuffer.append(detetedSignID)
        list = self.ringBuffer.get()
        list.reverse()
        if len(list) > 0:
            self.analyzescreen.label_IconTop.setPixmap(QtGui.QPixmap(list[0]))
        if len(list) > 1:
            self.analyzescreen.label_IconMid.setPixmap(QtGui.QPixmap(list[1]))
        if len(list) > 2:
            self.analyzescreen.label_IconBottom.setPixmap(QtGui.QPixmap(list[2]))



    def setVideoImage(self, img):
        self.analyzescreen.videoLayout.setPixmap(QtGui.QPixmap.fromImage(img))

    def startVideo(self):
        # create the video capture thread and handover filepath and the VzeGui class as object
        #self.thread = VideoThread(self.logic.getFilePath(), self)
        # call the real KI method later
        self.thread = VideoThreadKI(self.logic.getFilePath(), self)
        # start the thread
        self.thread.start()

    def activateResultBtn(self):
        self.analyzescreen.btn_showResult.setEnabled(True)
        self.analyzescreen.changeButtonEnabled()

    def deactivateResultBtn(self):
        self.analyzescreen.btn_showResult.setEnabled(False)
        self.analyzescreen.changeButtonEnabled()

    def initRingBuffer(self):
        self.ringBuffer = RingBuffer(3)


# Start Screen
class Ui_startscreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(Ui_startscreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("Start Screen")
        self.create_layout()
        self.create_button()
        self.create_label()
        self.create_spacer()
        self.add_items()

    def create_layout(self):
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lyth_headline = QtWidgets.QHBoxLayout()
        self.lyth_headline.setContentsMargins(20, -1, 20, 0)
        self.lyth_headline.setObjectName("lyth_headline")

        self.lytv_bigCenter = QtWidgets.QVBoxLayout()
        self.lytv_bigCenter.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytv_bigCenter.setContentsMargins(0, -1, 0, -1)
        self.lytv_bigCenter.setObjectName("lytv_bigCenter")
        self.lyth_smallText = QtWidgets.QHBoxLayout()
        self.lyth_smallText.setContentsMargins(-1, 0, -1, -1)
        self.lyth_smallText.setObjectName("lyth_smallText")

        self.lyth_bigBtn = QtWidgets.QHBoxLayout()
        self.lyth_bigBtn.setObjectName("lyth_bigBtn")

        self.lyth_smallBtn = QtWidgets.QHBoxLayout()
        self.lyth_smallBtn.setObjectName("lyth_smallBtn")

        self.lyth_bottom = QtWidgets.QHBoxLayout()
        self.lyth_bottom.setObjectName("lyth_bottom")

    def create_button(self):

        self.btn_info_startscreen = QtWidgets.QPushButton(self)
        self.btn_info_startscreen.setMinimumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_startscreen.setMaximumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_startscreen.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_startscreen.setIcon(icon)
        self.btn_info_startscreen.setIconSize(QtCore.QSize(constants.INFO_ICON_WIDTH, constants.INFO_ICON_HEIGTH))
        self.btn_info_startscreen.setObjectName("btn_info_startscreen")
        self.btn_info_startscreen.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_loadFile = QtWidgets.QPushButton(self)
        self.btn_loadFile.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONBIG_WIDTH, constants.BLUEBUTTONBIG_HEIGTH))
        self.btn_loadFile.setStyleSheet(styles.styleBluebuttonbig1)
        self.btn_loadFile.setText(("Datei auswählen"))
        self.btn_loadFile.setToolTip('Laden eines Videos oder Bildes')
        self.btn_loadFile.clicked.connect(self.gui.loadFile)

        self.btn_demoToDemo = QtWidgets.QPushButton(self)
        self.btn_demoToDemo.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONBIG_WIDTH, constants.BLUEBUTTONBIG_HEIGTH))
        self.btn_demoToDemo.setStyleSheet(styles.styleBluebuttonbig2)
        self.btn_demoToDemo.setText(("Demo auswählen"))
        self.btn_demoToDemo.setToolTip('Demo Videos wählen')
        self.btn_demoToDemo.clicked.connect(lambda: self.gui.change_screen(constants.DEMO_SCREEN))

    def create_label(self):

        self.lbl_willkommen = QtWidgets.QLabel(self)
        self.lbl_willkommen.setStyleSheet(styles.styleHeadlines)
        self.lbl_willkommen.setText(("Willkommen"))

    def create_spacer(self):

        self.spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem4 = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem7 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

    def add_items(self):

        self.lyth_headline.addWidget(self.lbl_willkommen)
        self.lyth_headline.addItem(self.spacerItem)
        self.lyth_headline.addWidget(self.btn_info_startscreen)
        self.verticalLayout_2.addLayout(self.lyth_headline)
        self.lyth_smallText.addItem(self.spacerItem1)
        self.lyth_smallText.addItem(self.spacerItem2)
        self.lytv_bigCenter.addLayout(self.lyth_smallText)
        self.lyth_bigBtn.addItem(self.spacerItem3)
        self.lyth_bigBtn.addWidget(self.btn_loadFile)
        self.lyth_bigBtn.addItem(self.spacerItem4)
        self.lyth_bigBtn.addItem(self.spacerItem5)
        self.lyth_bigBtn.addWidget(self.btn_demoToDemo)
        self.lyth_bigBtn.addItem(self.spacerItem6)
        self.lytv_bigCenter.addLayout(self.lyth_bigBtn)
        self.lyth_smallBtn.addItem(self.spacerItem7)
        self.lytv_bigCenter.addLayout(self.lyth_smallBtn)
        self.lytv_bigCenter.addItem(self.spacerItem8)
        self.verticalLayout_2.addLayout(self.lytv_bigCenter)
        self.lyth_bottom.addItem(self.spacerItem9)
        self.verticalLayout_2.addLayout(self.lyth_bottom)


# Demo Screen
class Ui_demoscreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(Ui_demoscreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("DemoScreen")
        self.create_layout()
        self.create_button()
        self.create_label()
        self.create_spacer()
        self.add_items()

    def create_layout(self):

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.lyth_headline_demoscreen = QtWidgets.QHBoxLayout()
        self.lyth_headline_demoscreen.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_demoscreen.setSpacing(constants.HEADLINE_SPACING)
        self.lyth_headline_demoscreen.setObjectName("lyth_headline_demoscreen")

        self.lytv_bigCenter_demoScreen = QtWidgets.QVBoxLayout()
        self.lytv_bigCenter_demoScreen.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytv_bigCenter_demoScreen.setContentsMargins(0, -1, 0, -1)
        self.lytv_bigCenter_demoScreen.setObjectName("lytv_bigCenter_demoScreen")

        self.lyth_smallText_Demo = QtWidgets.QHBoxLayout()
        self.lyth_smallText_Demo.setContentsMargins(20, 0, -1, -1)
        self.lyth_smallText_Demo.setObjectName("lyth_smallText_Demo")

        self.lyth_bigBtn_Demo = QtWidgets.QHBoxLayout()
        self.lyth_bigBtn_Demo.setObjectName("lyth_bigBtn_Demo")

        self.lyth_smallBtn_demoscreen = QtWidgets.QHBoxLayout()
        self.lyth_smallBtn_demoscreen.setObjectName("lyth_smallBtn_demoscreen")

        self.lyth_bottom_demoscreen = QtWidgets.QHBoxLayout()
        self.lyth_bottom_demoscreen.setObjectName("lyth_bottom_demoscreen")

    def create_button(self):
        self.btn_info_demoscreen = QtWidgets.QPushButton(self)
        self.btn_info_demoscreen.setMinimumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_demoscreen.setMaximumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_demoscreen.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_demoscreen.setIcon(icon)
        self.btn_info_demoscreen.setIconSize(QtCore.QSize(constants.INFO_ICON_WIDTH, constants.INFO_ICON_HEIGTH))
        self.btn_info_demoscreen.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_demoSonne = QtWidgets.QPushButton(self)
        self.btn_demoSonne.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONBIG_WIDTH, constants.BLUEBUTTONBIG_HEIGTH))
        self.btn_demoSonne.setStyleSheet(styles.styleBluebuttonbig3)
        self.btn_demoSonne.setText(("Video mit Sonne"))
        self.btn_demoSonne.clicked.connect(lambda: self.gui.loadDemoVideo(self.gui.demo_video1, constants.DEMO_ID_1))

        self.btn_demoRegen = QtWidgets.QPushButton(self)
        self.btn_demoRegen.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONBIG_WIDTH, constants.BLUEBUTTONBIG_HEIGTH))
        self.btn_demoRegen.setStyleSheet(styles.styleBluebuttonbig4)
        self.btn_demoRegen.setText(("Video mit Regen"))
        self.btn_demoRegen.clicked.connect(lambda: self.gui.loadDemoVideo(self.gui.demo_video2, constants.DEMO_ID_2))

        self.btn_dataSonne = QtWidgets.QPushButton(self)
        self.btn_dataSonne.setMinimumSize(QtCore.QSize(constants.SMALLBUTTON_WIDTH, constants.SMALLBUTTON_HEIGTH))
        self.btn_dataSonne.setMaximumSize(QtCore.QSize(constants.SMALLBUTTON_WIDTH, constants.SMALLBUTTON_HEIGTH))
        self.btn_dataSonne.setStyleSheet(styles.styleSmallButton)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/data_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_dataSonne.setIcon(icon1)
        self.btn_dataSonne.setIconSize(QtCore.QSize(constants.SMALLBUTTON_WIDTH, constants.SMALLBUTTON_HEIGTH))
        self.btn_dataSonne.clicked.connect(lambda: self.gui.create_DemoDataGrid(1))

        self.btn_dataRegen = QtWidgets.QPushButton(self)
        self.btn_dataRegen.setMinimumSize(QtCore.QSize(constants.SMALLBUTTON_WIDTH, constants.SMALLBUTTON_HEIGTH))
        self.btn_dataRegen.setMaximumSize(QtCore.QSize(constants.SMALLBUTTON_WIDTH, constants.SMALLBUTTON_HEIGTH))
        self.btn_dataRegen.setStyleSheet(styles.styleSmallButton)
        self.btn_dataRegen.setIcon(icon1)
        self.btn_dataRegen.setIconSize(QtCore.QSize(constants.SMALLBUTTON_WIDTH, constants.SMALLBUTTON_HEIGTH))
        self.btn_dataRegen.clicked.connect(lambda: self.gui.create_DemoDataGrid(2))

        self.btn_back_demoscreen = QtWidgets.QPushButton(self)
        self.btn_back_demoscreen.setMinimumSize(QtCore.QSize(constants.BACK_BUTTON_WIDTH, constants.BACK_BUTTON_HEIGTH))
        self.btn_back_demoscreen.setMaximumSize(QtCore.QSize(constants.BACK_BUTTON_WIDTH, constants.BACK_BUTTON_HEIGTH))
        self.btn_back_demoscreen.setStyleSheet(styles.styleSmallButton)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/back_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_demoscreen.setIcon(icon2)
        self.btn_back_demoscreen.setIconSize(QtCore.QSize(constants.BACK_ICON_WIDTH, constants.BACK_ICON_HEIGTH))
        self.btn_back_demoscreen.clicked.connect(lambda: self.gui.change_screen_back())

    def create_label(self):

        self.lbl_demo = QtWidgets.QLabel(self)
        self.lbl_demo.setStyleSheet(styles.styleHeadlines)
        self.lbl_demo.setObjectName("lbl_demo")
        self.lbl_demo.setText(("Demo"))

        self.label_demotext = QtWidgets.QLabel(self)
        self.label_demotext.setStyleSheet(styles.styleText1)
        self.label_demotext.setObjectName("label_demotext")
        self.label_demotext.setText(("Wählen Sie ein Demovideo aus"))

    def create_spacer(self):

        self.spacerItem10 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem14 = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem18 = QtWidgets.QSpacerItem(370, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem20 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.spacerItem21 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem23 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

    def add_items(self):

        self.lyth_headline_demoscreen.addWidget(self.lbl_demo)
        self.lyth_headline_demoscreen.addItem(self.spacerItem10)
        self.lyth_headline_demoscreen.addWidget(self.btn_info_demoscreen)
        self.verticalLayout_3.addLayout(self.lyth_headline_demoscreen)
        self.lyth_smallText_Demo.addWidget(self.label_demotext, 0, QtCore.Qt.AlignTop)
        self.lyth_smallText_Demo.addItem(self.spacerItem11)
        self.lyth_smallText_Demo.addItem(self.spacerItem12)
        self.lytv_bigCenter_demoScreen.addLayout(self.lyth_smallText_Demo)
        self.lyth_bigBtn_Demo.addItem(self.spacerItem13)
        self.lyth_bigBtn_Demo.addWidget(self.btn_demoSonne)
        self.lyth_bigBtn_Demo.addItem(self.spacerItem14)
        self.lyth_bigBtn_Demo.addItem(self.spacerItem15)
        self.lyth_bigBtn_Demo.addWidget(self.btn_demoRegen)
        self.lyth_bigBtn_Demo.addItem(self.spacerItem16)
        self.lytv_bigCenter_demoScreen.addLayout(self.lyth_bigBtn_Demo)
        self.lyth_smallBtn_demoscreen.addItem(self.spacerItem17)
        self.lyth_smallBtn_demoscreen.addWidget(self.btn_dataSonne)
        self.lyth_smallBtn_demoscreen.addItem(self.spacerItem18)
        self.lyth_smallBtn_demoscreen.addWidget(self.btn_dataRegen)
        self.lyth_smallBtn_demoscreen.addItem(self.spacerItem19)
        self.lyth_smallBtn_demoscreen.addItem(self.spacerItem20)
        self.lytv_bigCenter_demoScreen.addLayout(self.lyth_smallBtn_demoscreen)
        self.lytv_bigCenter_demoScreen.addItem(self.spacerItem21)
        self.verticalLayout_3.addLayout(self.lytv_bigCenter_demoScreen)
        self.lyth_bottom_demoscreen.addWidget(self.btn_back_demoscreen)
        self.lyth_bottom_demoscreen.addItem(self.spacerItem22)
        self.lyth_bottom_demoscreen.addItem(self.spacerItem23)
        self.lyth_bottom_demoscreen.addItem(self.spacerItem23)
        self.verticalLayout_3.addLayout(self.lyth_bottom_demoscreen)

# Preview Screen
class Ui_previewscreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(Ui_previewscreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("PreviewScreen")

        self.create_layout()
        self.create_button()
        self.create_label()
        self.create_spacer()
        self.create_otherObjects()
        self.add_items()

    def create_layout(self):
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.lyth_headline_previewScreen = QtWidgets.QHBoxLayout()
        self.lyth_headline_previewScreen.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_previewScreen.setSpacing(constants.HEADLINE_SPACING)
        self.lyth_headline_previewScreen.setObjectName("lyth_headline_previewScreen")

        self.lytv_bigCenter_previewScreen = QtWidgets.QVBoxLayout()
        self.lytv_bigCenter_previewScreen.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytv_bigCenter_previewScreen.setContentsMargins(0, -1, 0, -1)
        self.lytv_bigCenter_previewScreen.setObjectName("lytv_bigCenter_previewScreen")
        self.lyth_smallText_previewScreen = QtWidgets.QHBoxLayout()
        self.lyth_smallText_previewScreen.setContentsMargins(20, 0, -1, -1)
        self.lyth_smallText_previewScreen.setObjectName("lyth_smallText_previewScreen")

        self.lyth_centerBig = QtWidgets.QHBoxLayout()
        self.lyth_centerBig.setObjectName("lyth_centerBig")

        self.lyth_blwCenter = QtWidgets.QHBoxLayout()
        self.lyth_blwCenter.setObjectName("lyth_blwCenter")

        self.lyth_bottom_previewScreen = QtWidgets.QHBoxLayout()
        self.lyth_bottom_previewScreen.setContentsMargins(-1, -1, 20, -1)
        self.lyth_bottom_previewScreen.setObjectName("lyth_bottom_previewScreen")

    def create_button(self):
        self.btn_info_previewScreen = QtWidgets.QPushButton(self)
        self.btn_info_previewScreen.setMinimumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_previewScreen.setMaximumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_previewScreen.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_previewScreen.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_previewScreen.setIcon(icon)
        self.btn_info_previewScreen.setIconSize(QtCore.QSize(constants.INFO_ICON_WIDTH, constants.INFO_ICON_HEIGTH))
        self.btn_info_previewScreen.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_back_previewScreen = QtWidgets.QPushButton(self)
        self.btn_back_previewScreen.setMinimumSize(QtCore.QSize(constants.BACK_BUTTON_WIDTH, constants.BACK_BUTTON_HEIGTH))
        self.btn_back_previewScreen.setMaximumSize(QtCore.QSize(constants.BACK_BUTTON_WIDTH, constants.BACK_BUTTON_HEIGTH))
        self.btn_back_previewScreen.setStyleSheet(styles.styleSmallButton)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/back_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_previewScreen.setIcon(icon2)
        self.btn_back_previewScreen.setIconSize(QtCore.QSize(constants.BACK_ICON_WIDTH, constants.BACK_ICON_HEIGTH))
        self.btn_back_previewScreen.setObjectName("btn_back_previewScreen")
        self.btn_back_previewScreen.clicked.connect(lambda: self.gui.change_screen_back())

        self.btn_next_preview = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_next_preview.sizePolicy().hasHeightForWidth())
        self.btn_next_preview.setSizePolicy(sizePolicy)
        self.btn_next_preview.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_next_preview.setMaximumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_next_preview.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_next_preview.setCheckable(False)
        self.btn_next_preview.setFlat(False)
        self.btn_next_preview.setText("Weiter")
        self.btn_next_preview.clicked.connect(lambda: self.gui.change_screen(constants.DI_SCREEN))

    def create_label(self):
        self.lbl_headline_preview = QtWidgets.QLabel(self)
        self.lbl_headline_preview.setStyleSheet(styles.styleHeadlines)
        self.lbl_headline_preview.setText("Datei Analyze")

        self.label_preview = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_preview.sizePolicy().hasHeightForWidth())
        self.label_preview.setSizePolicy(sizePolicy)
        self.label_preview.setStyleSheet(styles.styleText1)
        self.label_preview.setText("Vorschau")

        self.label_loadSuccess = QtWidgets.QLabel(self)
        self.label_loadSuccess.setStyleSheet(styles.styleText1)
        self.label_loadSuccess.setText("Datei erfolgreich geladen. ")

    def create_spacer(self):

        self.spacerItem24 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem25 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem26 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem27 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem28 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem29 = QtWidgets.QSpacerItem(0, 450, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem30 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem31 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem32 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

    def create_otherObjects(self):
        self.imageLayout = QtWidgets.QLabel(self)
        self.imageLayout.setText("")
        self.imageLayout.setMinimumSize(QtCore.QSize(constants.PREVIEWIMAGE_WIDTH, constants.PREVIEWIMAGE_HEIGTH))
        self.imageLayout.setMaximumSize(QtCore.QSize(constants.PREVIEWIMAGE_WIDTH, constants.PREVIEWIMAGE_HEIGTH))
        # self.graphicsPreview = QtWidgets.QGraphicsView(self)
        # self.graphicsPreview.setMinimumSize(QtCore.QSize(constants.PREVIEWIMAGE_WIDTH, constants.PREVIEWIMAGE_HEIGTH))
        # self.graphicsPreview.setMaximumSize(QtCore.QSize(constants.PREVIEWIMAGE_WIDTH, constants.PREVIEWIMAGE_HEIGTH))
        # self.graphicsPreview.setObjectName("graphicsPreview")

    def add_items(self):
        self.lyth_headline_previewScreen.addWidget(self.lbl_headline_preview)
        self.lyth_headline_previewScreen.addItem(self.spacerItem24)
        self.lyth_headline_previewScreen.addWidget(self.btn_info_previewScreen)
        self.verticalLayout_4.addLayout(self.lyth_headline_previewScreen)
        self.lyth_smallText_previewScreen.addWidget(self.label_preview, 0, QtCore.Qt.AlignTop)
        self.lyth_smallText_previewScreen.addItem(self.spacerItem25)
        self.lyth_smallText_previewScreen.addItem(self.spacerItem26)
        self.lytv_bigCenter_previewScreen.addLayout(self.lyth_smallText_previewScreen)
        self.lyth_centerBig.addItem(self.spacerItem27)
        #self.lyth_centerBig.addWidget(self.graphicsPreview)
        self.lyth_centerBig.addWidget(self.imageLayout)
        self.lyth_centerBig.addItem(self.spacerItem28)
        self.lyth_centerBig.addItem(self.spacerItem29)
        self.lytv_bigCenter_previewScreen.addLayout(self.lyth_centerBig)
        self.lytv_bigCenter_previewScreen.addLayout(self.lyth_blwCenter)
        self.lytv_bigCenter_previewScreen.addItem(self.spacerItem30)
        self.lytv_bigCenter_previewScreen.addWidget(self.label_loadSuccess, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_4.addLayout(self.lytv_bigCenter_previewScreen)
        self.lyth_bottom_previewScreen.addWidget(self.btn_back_previewScreen)
        self.lyth_bottom_previewScreen.addItem(self.spacerItem31)
        self.lyth_bottom_previewScreen.addItem(self.spacerItem32)
        self.lyth_bottom_previewScreen.addWidget(self.btn_next_preview)
        self.verticalLayout_4.addLayout(self.lyth_bottom_previewScreen)


# DI Screen
class Ui_DIScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(Ui_DIScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("DIScreen")

        self.create_layout()
        self.create_button()
        self.create_label()
        self.create_spacer()
        self.create_gridContent()
        self.add_items()

    def create_layout(self):
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.lyth_headline_DIScreen = QtWidgets.QHBoxLayout()
        self.lyth_headline_DIScreen.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_DIScreen.setSpacing(constants.HEADLINE_SPACING)
        self.lyth_headline_DIScreen.setObjectName("lyth_headline_DIScreen")

        self.lyth_smallText_DIScreen = QtWidgets.QHBoxLayout()
        self.lyth_smallText_DIScreen.setContentsMargins(20, 0, -1, -1)
        self.lyth_smallText_DIScreen.setObjectName("lyth_smallText_DIScreen")

        self.lyth_bigGrid_DiScreen = QtWidgets.QHBoxLayout()
        self.lyth_bigGrid_DiScreen.setContentsMargins(0, 9, -1, 20)
        self.lyth_bigGrid_DiScreen.setObjectName("lyth_bigGrid_DiScreen")

        self.scrollArea_DIScreen = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.scrollArea_DIScreen.sizePolicy().hasHeightForWidth())
        self.scrollArea_DIScreen.setSizePolicy(sizePolicy)
        self.scrollArea_DIScreen.setMinimumSize(QtCore.QSize(constants.SCROLLAREA_OUTER_MIN_WIDTH, constants.SCROLLAREA_MIN_HEIGTH))
        self.scrollArea_DIScreen.setMaximumSize(QtCore.QSize(constants.SCROLLAREA_OUTER_MAX_WIDTH, constants.SCROLLAREA_MAX_HEIGTH))
        self.scrollArea_DIScreen.setSizeIncrement(QtCore.QSize(0, 0))
        self.scrollArea_DIScreen.setWidgetResizable(True)
        self.scrollArea_DIScreen.setObjectName("scrollArea_DIScreen")

        self.scrollAreaWidget_DIScreen = QtWidgets.QWidget()
        self.scrollAreaWidget_DIScreen.setGeometry(QtCore.QRect(0, 0, constants.SCROLLAREA_INNER_WIDTH, 816))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidget_DIScreen.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidget_DIScreen.setSizePolicy(sizePolicy)
        self.scrollAreaWidget_DIScreen.setMinimumSize(QtCore.QSize(constants.SCROLLAREA_INNER_WIDTH, constants.SCROLLAREA_MIN_HEIGTH))
        self.scrollAreaWidget_DIScreen.setMaximumSize(QtCore.QSize(constants.SCROLLAREA_INNER_WIDTH, constants.SCROLLAREA_MAX_HEIGTH))
        self.scrollAreaWidget_DIScreen.setObjectName("scrollAreaWidget_DIScreen")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidget_DIScreen)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.gridLayout_DIScreen = QtWidgets.QGridLayout()
        self.gridLayout_DIScreen.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_DIScreen.setContentsMargins(0, 10, 0, 10)
        self.gridLayout_DIScreen.setHorizontalSpacing(40)
        self.gridLayout_DIScreen.setVerticalSpacing(25)
        self.gridLayout_DIScreen.setObjectName("gridLayout_DIScreen")

        self.lyth_bottom_DIScreen = QtWidgets.QHBoxLayout()
        self.lyth_bottom_DIScreen.setContentsMargins(-1, -1, 0, -1)
        self.lyth_bottom_DIScreen.setObjectName("lyth_bottom_DIScreen")

    def create_button(self):
        self.btn_info_DIScreen = QtWidgets.QPushButton(self)
        self.btn_info_DIScreen.setMinimumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_DIScreen.setMaximumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_DIScreen.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_DIScreen.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_DIScreen.setIcon(icon)
        self.btn_info_DIScreen.setIconSize(QtCore.QSize(constants.INFO_ICON_WIDTH, constants.INFO_ICON_HEIGTH))
        self.btn_info_DIScreen.setObjectName("btn_info_DIScreen")
        self.btn_info_DIScreen.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_back_DI = QtWidgets.QPushButton(self)
        self.btn_back_DI.setMinimumSize(QtCore.QSize(constants.BACK_BUTTON_WIDTH, constants.BACK_BUTTON_HEIGTH))
        self.btn_back_DI.setMaximumSize(QtCore.QSize(constants.BACK_BUTTON_WIDTH, constants.BACK_BUTTON_HEIGTH))
        self.btn_back_DI.setStyleSheet(styles.styleSmallButton)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/back_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_DI.setIcon(icon2)
        self.btn_back_DI.setIconSize(QtCore.QSize(constants.BACK_ICON_WIDTH, constants.BACK_ICON_HEIGTH))
        self.btn_back_DI.setCheckable(True)
        self.btn_back_DI.setObjectName("btn_back_DI")
        self.btn_back_DI.clicked.connect(lambda: self.gui.change_screen_back())

        self.btn_reset = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_reset.sizePolicy().hasHeightForWidth())
        self.btn_reset.setSizePolicy(sizePolicy)
        self.btn_reset.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_reset.setMaximumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_reset.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_reset.setText("Zurücksetzen")
        self.btn_reset.setCheckable(False)
        self.btn_reset.setFlat(False)
        self.btn_reset.setObjectName("btn_reset")
        self.btn_reset.clicked.connect(lambda: self.reset_gridContent())

        self.btn_skip = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_skip.sizePolicy().hasHeightForWidth())
        self.btn_skip.setSizePolicy(sizePolicy)
        self.btn_skip.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_skip.setMaximumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_skip.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_skip.setText("Überspringen")
        self.btn_skip.setCheckable(False)
        self.btn_skip.setFlat(False)
        self.btn_skip.setObjectName("btn_skip")
        self.btn_skip.clicked.connect(lambda: self.skip_dataInput())


        self.btn_DInext = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_DInext.sizePolicy().hasHeightForWidth())
        self.btn_DInext.setSizePolicy(sizePolicy)
        self.btn_DInext.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_DInext.setMaximumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_DInext.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_DInext.setText("Weiter")
        self.btn_DInext.setCheckable(False)
        self.btn_DInext.setFlat(False)
        self.btn_DInext.setObjectName("btn_DInext")
        self.btn_DInext.clicked.connect(lambda: self.save_gridContent())

    def create_label(self):
        self.lbl_headline_DIScreen = QtWidgets.QLabel(self)
        self.lbl_headline_DIScreen.setStyleSheet(styles.styleHeadlines)
        self.lbl_headline_DIScreen.setText("Datei Analyse")
        self.lbl_headline_DIScreen.setObjectName("lbl_headline_DIScreen")

        self.label_DIScreen_smalltext = QtWidgets.QLabel(self)
        self.label_DIScreen_smalltext.setStyleSheet(styles.styleText1)
        self.label_DIScreen_smalltext.setText("Anzahl der Schilder eingeben (Optional)")
        self.label_DIScreen_smalltext.setObjectName("label_DIScreen_smalltext")
    
    def create_gridContent(self):

        row_count = 0
        column_count = 0
        sign_count = 0
        
        while row_count <= constants.DISCREEN_ROWS:    
            while column_count <= constants.DISCREEN_COLUMNS:
                if sign_count<constants.TOTAL_NUMBER_SIGNS:
                    #print("sign: row_count:"+ str(row_count) + " column_count:"+ str(column_count) + " sign_count:"+ str(sign_count))
                    #create signs
                    self.name_sign = "lbl_sign_"+ str(sign_count)
                    self.sign_id = ":/signs/" + str(sign_count)
                    self.name_sign = QtWidgets.QLabel(self.scrollAreaWidget_DIScreen)
                    self.name_sign.setMinimumSize(QtCore.QSize(constants.SIGN_WIDTH, constants.SIGN_HEIGTH))
                    self.name_sign.setMaximumSize(QtCore.QSize(constants.SIGN_WIDTH, constants.SIGN_HEIGTH))
                    self.name_sign.setObjectName(str(sign_count))
                    self.name_sign.setPixmap(QtGui.QPixmap(self.sign_id))
                    self.name_sign.setScaledContents(True)

                    self.gridLayout_DIScreen.addWidget(self.name_sign, row_count,column_count,1,1)
                    
                    #column_count++ to create the spinbox next to sign (label)
                    column_count =column_count+1

                    # create spinboxes 
                    # print("sb: row_count:"+ str(row_count) + " column_count:"+ str(column_count) + " sign_count:"+ str(sign_count))
                    self.name_sb = "spinBox_"+ str(sign_count)
                    self.name_sb = QtWidgets.QSpinBox(self.scrollAreaWidget_DIScreen)
                    self.name_sb.setMinimumSize(QtCore.QSize(constants.SPINBOX_WIDTH, constants.SPINBOX_HEIGTH))
                    self.name_sb.setMaximumSize(QtCore.QSize(constants.SPINBOX_WIDTH, constants.SPINBOX_HEIGTH))
                    self.name_sb.setStyleSheet(styles.styleSpinBox)
                    self.name_sb.setValue(0)
                    self.gridLayout_DIScreen.addWidget(self.name_sb, row_count, column_count, 1, 1)
                    
                column_count = column_count+1
                sign_count = sign_count+1
            column_count = 0
            row_count = row_count+1

    def create_spacer(self):
        self.spacerItem33 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem34 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem35 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.spacerItem36 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem37 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem38 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.spacerItem39 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem40 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem41 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem42 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def add_items(self):
        self.lyth_headline_DIScreen.addWidget(self.lbl_headline_DIScreen)
        self.lyth_headline_DIScreen.addItem(self.spacerItem33)
        self.lyth_headline_DIScreen.addWidget(self.btn_info_DIScreen)
        self.verticalLayout_11.addLayout(self.lyth_headline_DIScreen)
        self.lyth_smallText_DIScreen.addWidget(self.label_DIScreen_smalltext, 0, QtCore.Qt.AlignTop)
        self.lyth_smallText_DIScreen.addItem(self.spacerItem34)
        self.lyth_smallText_DIScreen.addItem(self.spacerItem35)
        self.verticalLayout_11.addLayout(self.lyth_smallText_DIScreen)
        self.lyth_bigGrid_DiScreen.addItem(self.spacerItem36)
        self.horizontalLayout_2.addLayout(self.gridLayout_DIScreen)
        self.scrollArea_DIScreen.setWidget(self.scrollAreaWidget_DIScreen)
        self.lyth_bigGrid_DiScreen.addWidget(self.scrollArea_DIScreen)
        self.lyth_bigGrid_DiScreen.addItem(self.spacerItem37)
        self.verticalLayout_11.addLayout(self.lyth_bigGrid_DiScreen)
        self.lyth_bottom_DIScreen.addWidget(self.btn_back_DI)
        self.lyth_bottom_DIScreen.addItem(self.spacerItem38)
        self.lyth_bottom_DIScreen.addItem(self.spacerItem39)
        self.lyth_bottom_DIScreen.addWidget(self.btn_reset)
        self.lyth_bottom_DIScreen.addItem(self.spacerItem40)
        self.lyth_bottom_DIScreen.addWidget(self.btn_skip)
        self.lyth_bottom_DIScreen.addItem(self.spacerItem41)
        self.lyth_bottom_DIScreen.addWidget(self.btn_DInext)
        self.lyth_bottom_DIScreen.addItem(self.spacerItem42)
        self.verticalLayout_11.addLayout(self.lyth_bottom_DIScreen)

    def save_gridContent(self):
        entry_count = self.gridLayout_DIScreen.count() -1
        item_count = 0
        array_count = 0
    
        while item_count < entry_count:
            labelItem = self.gridLayout_DIScreen.itemAt(item_count).widget()
            labelItemValue = str(labelItem.objectName())
            self.logic.setDataArray(array_count, constants.DATA_ARRAY_SIGN_ID, labelItemValue)
            
            item_count = item_count+1
            
            spinboxItem = self.gridLayout_DIScreen.itemAt(item_count).widget()
            spinboxItemValue = spinboxItem.value()
            self.logic.setDataArray(array_count, constants.DATA_ARRAY_SIGN_INPUT, spinboxItemValue)

            #Temporär die Ergebniszeile alles auf spinboxItemValue setzen
            #self.logic.setDataArray(array_count, constants.DATA_ARRAY_SIGN_DETECTED, spinboxItemValue)

            item_count = item_count+1
            array_count = array_count+1

        #Testausgabe des gesamten Arrays
        # for j in range(len(self.logic.array_dataInput[constants.DATA_ARRAY_SIGN_ID])):
        #     print(self.logic.getDataArray(j, constants.DATA_ARRAY_SIGN_ID), end=' ')
        #     print(self.logic.getDataArray(j, constants.DATA_ARRAY_SIGN_INPUT), end=' ')
        #     print(self.logic.getDataArray(j, constants.DATA_ARRAY_SIGN_DETECTED), end=' ')
        #     print()

        self.check_gridContent()

    def reset_gridContent(self):
        entry_count = self.gridLayout_DIScreen.count() -1
        item_count = 0
        array_count = 0
    
        while(item_count < entry_count):
            # labelItem = self.gridLayout_DIScreen.itemAt(item_count).widget()
            # labelItemValue = str(labelItem.objectName())
            # print("Label: " + str(labelItem))
            # print("Label Value: " + labelItemValue)
            # self.logic.setDataArray(array_count, constants.DATA_ARRAY_SIGN_ID, labelItemValue)
            item_count = item_count+1
            
            spinboxItem = self.gridLayout_DIScreen.itemAt(item_count).widget()
            # print("SpinBox: " + str(spinboxItem))
            # spinboxItemValue = str(spinboxItem.value())
            # print("SpinBox Value Before: " + spinboxItemValue)
            spinboxItem.setValue(0)
            spinboxItemValue = spinboxItem.value()
            self.logic.setDataArray(array_count, constants.DATA_ARRAY_SIGN_INPUT, spinboxItemValue)
            item_count = item_count+1
            array_count = array_count+1

    def check_gridContent(self):
        
        emptyCheck = True
        
        for array_count in range(len(self.logic.array_dataInput[constants.DATA_ARRAY_SIGN_ID])):
            sign_count = self.logic.getDataArray(array_count, constants.DATA_ARRAY_SIGN_INPUT)
            if sign_count > 0:
                emptyCheck = False
           
        if emptyCheck:
            title = "Keine Daten eingegeben"
            message = "Sie haben keine Daten eingegeben!\nDas bedeutet, dass in Ihrem Video keine Verkehrszeichen vorkommen!\nIst dies der Fall oder wenn Sie keinen Vergleich wünschen, nutzen Sie bitte den Button 'Überspringen'"
            self.gui.showPopup(title,message)
        else:
            self.logic.setCompareResult(True)
            self.gui.change_screen(constants.ANALYZE_PV_SCREEN)

    def skip_dataInput(self):
        self.logic.setCompareResult(False)

        entry_count = self.gridLayout_DIScreen.count() -1
        item_count = 0
        array_count = 0
    
        while item_count < entry_count:
            labelItem = self.gridLayout_DIScreen.itemAt(item_count).widget()
            labelItemValue = str(labelItem.objectName())
            self.logic.setDataArray(array_count, constants.DATA_ARRAY_SIGN_ID, labelItemValue)
            
            item_count = item_count+1
            
            self.logic.setDataArray(array_count, constants.DATA_ARRAY_SIGN_INPUT, 0)

            item_count = item_count+1
            array_count = array_count+1

        #Testausgabe des gesamten Arrays
        # for j in range(len(self.logic.array_dataInput[constants.DATA_ARRAY_SIGN_ID])):
        #     print(self.logic.getDataArray(j, constants.DATA_ARRAY_SIGN_ID), end=' ')
        #     print(self.logic.getDataArray(j, constants.DATA_ARRAY_SIGN_INPUT), end=' ')
        #     print(self.logic.getDataArray(j, constants.DATA_ARRAY_SIGN_DETECTED), end=' ')
        #     print()

        self.gui.change_screen(constants.ANALYZE_PV_SCREEN)

            
        

# Analyze Preview Screen
class Ui_analyzePvScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(Ui_analyzePvScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("AnalyzePreviewScreen")

        self.create_layout()
        self.create_button()
        self.create_label()
        self.create_preview()
        self.create_spacer()
        self.add_items()        

    def create_layout(self):
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lyth_headline_AnalyzePreview = QtWidgets.QHBoxLayout()
        self.lyth_headline_AnalyzePreview.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_AnalyzePreview.setSpacing(constants.HEADLINE_SPACING)
        self.lyth_headline_AnalyzePreview.setObjectName("lyth_headline_AnalyzePreview")

        self.verticalLayout_5.addLayout(self.lyth_headline_AnalyzePreview)
        self.lytv_bigCenter_AnalyzePreview = QtWidgets.QVBoxLayout()
        self.lytv_bigCenter_AnalyzePreview.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytv_bigCenter_AnalyzePreview.setContentsMargins(0, -1, 0, -1)
        self.lytv_bigCenter_AnalyzePreview.setObjectName("lytv_bigCenter_AnalyzePreview")
        self.lyth_smallText_AnalyzePreview = QtWidgets.QHBoxLayout()
        self.lyth_smallText_AnalyzePreview.setContentsMargins(20, 0, -1, -1)
        self.lyth_smallText_AnalyzePreview.setObjectName("lyth_smallText_AnalyzePreview")

        self.lyth_centerBig_AnalyzePreview = QtWidgets.QHBoxLayout()
        self.lyth_centerBig_AnalyzePreview.setObjectName("lyth_centerBig_AnalyzePreview")

        self.lyth_blwCenter_AnalyzePreview = QtWidgets.QHBoxLayout()
        self.lyth_blwCenter_AnalyzePreview.setObjectName("lyth_blwCenter_AnalyzePreview")

        self.lyth_bottom_AnalyzePreview = QtWidgets.QHBoxLayout()
        self.lyth_bottom_AnalyzePreview.setContentsMargins(-1, -1, 40, -1)
        self.lyth_bottom_AnalyzePreview.setObjectName("lyth_bottom_AnalyzePreview") 

    def create_button(self):
        self.btn_info_AnalyzePreview = QtWidgets.QPushButton(self)
        self.btn_info_AnalyzePreview.setMinimumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_AnalyzePreview.setMaximumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_AnalyzePreview.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_AnalyzePreview.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_AnalyzePreview.setIcon(icon)
        self.btn_info_AnalyzePreview.setIconSize(QtCore.QSize(constants.INFO_ICON_WIDTH, constants.INFO_ICON_HEIGTH))
        self.btn_info_AnalyzePreview.setObjectName("btn_info_AnalyzePreview")
        self.btn_info_AnalyzePreview.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_back_AnalyzePreview = QtWidgets.QPushButton(self)
        self.btn_back_AnalyzePreview.setMinimumSize(QtCore.QSize(constants.BACK_BUTTON_WIDTH, constants.BACK_BUTTON_HEIGTH))
        self.btn_back_AnalyzePreview.setMaximumSize(QtCore.QSize(constants.BACK_BUTTON_WIDTH, constants.BACK_BUTTON_HEIGTH))
        self.btn_back_AnalyzePreview.setStyleSheet(styles.styleSmallButton)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/back_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_AnalyzePreview.setIcon(icon2)
        self.btn_back_AnalyzePreview.setIconSize(QtCore.QSize(constants.BACK_ICON_WIDTH, constants.BACK_ICON_HEIGTH))
        self.btn_back_AnalyzePreview.setCheckable(True)
        self.btn_back_AnalyzePreview.setObjectName("btn_back_AnalyzePreview")
        self.btn_back_AnalyzePreview.clicked.connect(lambda: self.gui.change_screen_back())

        self.btn_startAnalyze = QtWidgets.QPushButton(self)
        self.btn_startAnalyze.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_startAnalyze.setMaximumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_startAnalyze.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_startAnalyze.setText("Analyse starten")
        self.btn_startAnalyze.setCheckable(False)
        self.btn_startAnalyze.setFlat(False)
        self.btn_startAnalyze.setObjectName("btn_startAnalyze")
        self.btn_startAnalyze.clicked.connect(lambda: self.gui.change_screen(constants.ANALYZE_SCREEN))
        self.btn_startAnalyze.clicked.connect(self.gui.startVideo)


    def create_label(self):
        self.lbl_headline_AnalyzePreview = QtWidgets.QLabel(self)
        self.lbl_headline_AnalyzePreview.setStyleSheet(styles.styleHeadlines)
        self.lbl_headline_AnalyzePreview.setText("Datei Analyse")
        self.lbl_headline_AnalyzePreview.setObjectName("lbl_headline_AnalyzePreview")

        self.label_AnalyzePreview = QtWidgets.QLabel(self)
        self.label_AnalyzePreview.setStyleSheet(styles.styleText1)
        self.label_AnalyzePreview.setText("Vorschau")
        self.label_AnalyzePreview.setObjectName("label_AnalyzePreview")

    def create_preview(self):
        self.imageLayout = QtWidgets.QLabel(self)
        self.imageLayout.setText("")
        self.imageLayout.setMinimumSize(QtCore.QSize(constants.PREVIEWIMAGE_WIDTH, constants.PREVIEWIMAGE_HEIGTH))
        self.imageLayout.setMaximumSize(QtCore.QSize(constants.PREVIEWIMAGE_WIDTH, constants.PREVIEWIMAGE_HEIGTH))
        # self.graphicsAnalyzePreview = QtWidgets.QGraphicsView(self)
        # self.graphicsAnalyzePreview.setMinimumSize(QtCore.QSize(constants.PREVIEWIMAGE_WIDTH, constants.PREVIEWIMAGE_HEIGTH))
        # self.graphicsAnalyzePreview.setMaximumSize(QtCore.QSize(constants.PREVIEWIMAGE_WIDTH, constants.PREVIEWIMAGE_HEIGTH))
        # self.graphicsAnalyzePreview.setObjectName("graphicsAnalyzePreview")
        

    def create_spacer(self):
        self.spacerItem43 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem44 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem45 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem46 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem47 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem48 = QtWidgets.QSpacerItem(0, 450, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem49 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem50 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.spacerItem51 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem52 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def add_items(self):
        self.lyth_headline_AnalyzePreview.addWidget(self.lbl_headline_AnalyzePreview)
        self.lyth_headline_AnalyzePreview.addItem(self.spacerItem43)        
        self.lyth_headline_AnalyzePreview.addWidget(self.btn_info_AnalyzePreview)
        self.lyth_smallText_AnalyzePreview.addWidget(self.label_AnalyzePreview, 0, QtCore.Qt.AlignTop)
        self.lyth_smallText_AnalyzePreview.addItem(self.spacerItem44)
        self.lyth_smallText_AnalyzePreview.addItem(self.spacerItem45)
        self.lytv_bigCenter_AnalyzePreview.addLayout(self.lyth_smallText_AnalyzePreview)
        self.lyth_centerBig_AnalyzePreview.addItem(self.spacerItem46)
        #self.lyth_centerBig_AnalyzePreview.addWidget(self.graphicsAnalyzePreview)
        self.lyth_centerBig_AnalyzePreview.addWidget(self.imageLayout)
        self.lyth_centerBig_AnalyzePreview.addItem(self.spacerItem47)
        self.lyth_centerBig_AnalyzePreview.addItem(self.spacerItem48)
        self.lytv_bigCenter_AnalyzePreview.addLayout(self.lyth_centerBig_AnalyzePreview)
        self.lytv_bigCenter_AnalyzePreview.addLayout(self.lyth_blwCenter_AnalyzePreview)
        self.lytv_bigCenter_AnalyzePreview.addItem(self.spacerItem49)
        self.verticalLayout_5.addLayout(self.lytv_bigCenter_AnalyzePreview)
        self.lyth_bottom_AnalyzePreview.addWidget(self.btn_back_AnalyzePreview)
        self.lyth_bottom_AnalyzePreview.addItem(self.spacerItem50)
        self.lyth_bottom_AnalyzePreview.addItem(self.spacerItem51)
        self.lyth_bottom_AnalyzePreview.addWidget(self.btn_startAnalyze)
        self.lyth_bottom_AnalyzePreview.addItem(self.spacerItem52)
        self.verticalLayout_5.addLayout(self.lyth_bottom_AnalyzePreview)
        

# Analyze Screen
class Ui_analyzeScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(Ui_analyzeScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("AnalyseScreen")

        self.create_layout()
        self.create_button()
        self.create_label()
        self.create_preview()
        self.create_spacer()
        self.add_items()        

    def create_layout(self):
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lyth_headline_Analyze = QtWidgets.QHBoxLayout()
        self.lyth_headline_Analyze.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_Analyze.setSpacing(constants.HEADLINE_SPACING)
        self.lyth_headline_Analyze.setObjectName("lyth_headline_Analyze")

        self.lytv_bigCenter_Analyze = QtWidgets.QVBoxLayout()
        self.lytv_bigCenter_Analyze.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytv_bigCenter_Analyze.setContentsMargins(0, -1, 0, -1)
        self.lytv_bigCenter_Analyze.setObjectName("lytv_bigCenter_Analyze")

        self.lyth_smallText_Analyze = QtWidgets.QHBoxLayout()
        self.lyth_smallText_Analyze.setContentsMargins(20, 0, -1, -1)
        self.lyth_smallText_Analyze.setObjectName("lyth_smallText_Analyze")

        self.lyth_centerBig_Analyze = QtWidgets.QHBoxLayout()
        self.lyth_centerBig_Analyze.setObjectName("lyth_centerBig_Analyze")

        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(-1, -1, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.lyth_blwCenter_Analyze = QtWidgets.QHBoxLayout()
        self.lyth_blwCenter_Analyze.setObjectName("lyth_blwCenter_Analyze")

        self.lyth_bottom_Analyze = QtWidgets.QHBoxLayout()
        self.lyth_bottom_Analyze.setContentsMargins(-1, -1, 0, -1)
        self.lyth_bottom_Analyze.setSpacing(0)
        self.lyth_bottom_Analyze.setObjectName("lyth_bottom_Analyze")


    def create_button(self):
        self.btn_info_Analyze = QtWidgets.QPushButton(self)
        self.btn_info_Analyze.setMinimumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_Analyze.setMaximumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_Analyze.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_Analyze.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_Analyze.setIcon(icon)
        self.btn_info_Analyze.setIconSize(QtCore.QSize(constants.INFO_ICON_WIDTH, constants.INFO_ICON_HEIGTH))
        self.btn_info_Analyze.setObjectName("btn_info_Analyze")
        self.btn_info_Analyze.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_cancelAnalyze = QtWidgets.QPushButton(self)
        self.btn_cancelAnalyze.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_cancelAnalyze.setMaximumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_cancelAnalyze.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_cancelAnalyze.setText("Abbrechen")
        self.btn_cancelAnalyze.setObjectName("btn_cancelAnalyze")
        self.btn_cancelAnalyze.clicked.connect(self.gui.cancel_Analyze)

        self.btn_showResult = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_showResult.sizePolicy().hasHeightForWidth())
        self.btn_showResult.setSizePolicy(sizePolicy)
        self.btn_showResult.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_showResult.setMaximumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_showResult.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_showResult.setText("Zur Auswertung")
        self.btn_showResult.setEnabled(False)
        self.btn_showResult.setObjectName("btn_showResult")
        self.btn_showResult.clicked.connect(self.gui.show_Result)



    def create_label(self):
        self.lbl_headline_Analyze = QtWidgets.QLabel(self)
        self.lbl_headline_Analyze.setStyleSheet(styles.styleHeadlines)
        self.lbl_headline_Analyze.setText("Datei Analyse")
        self.lbl_headline_Analyze.setObjectName("lbl_headline_Analyze")

        self.label_Analyze = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Analyze.sizePolicy().hasHeightForWidth())
        self.label_Analyze.setSizePolicy(sizePolicy)
        self.label_Analyze.setStyleSheet(styles.styleText1)
        self.label_Analyze.setText("Analyse läuft...")
        self.label_Analyze.setObjectName("label_Analyze")

        self.label_IconTop = QtWidgets.QLabel(self)
        self.label_IconTop.setMinimumSize(QtCore.QSize(constants.ANALYZE_SCREEN_ICON_WIDTH, constants.ANALYZE_SCREEN_ICON_HEIGTH))
        self.label_IconTop.setMaximumSize(QtCore.QSize(constants.ANALYZE_SCREEN_ICON_WIDTH, constants.ANALYZE_SCREEN_ICON_HEIGTH))
        self.label_IconTop.setObjectName("label_IconTop")
        self.label_IconTop.setScaledContents(True)

        self.label_IconMid = QtWidgets.QLabel(self)
        self.label_IconMid.setMinimumSize(QtCore.QSize(constants.ANALYZE_SCREEN_ICON_WIDTH, constants.ANALYZE_SCREEN_ICON_HEIGTH))
        self.label_IconMid.setMaximumSize(QtCore.QSize(constants.ANALYZE_SCREEN_ICON_WIDTH, constants.ANALYZE_SCREEN_ICON_HEIGTH))
        self.label_IconMid.setObjectName("label_IconMid")
        self.label_IconMid.setScaledContents(True)

        self.label_IconBottom = QtWidgets.QLabel(self)
        self.label_IconBottom.setMinimumSize(QtCore.QSize(constants.ANALYZE_SCREEN_ICON_WIDTH, constants.ANALYZE_SCREEN_ICON_HEIGTH))
        self.label_IconBottom.setMaximumSize(QtCore.QSize(constants.ANALYZE_SCREEN_ICON_WIDTH, constants.ANALYZE_SCREEN_ICON_HEIGTH))
        self.label_IconBottom.setObjectName("label_IconBottom")
        self.label_IconBottom.setScaledContents(True)


    def create_preview(self):

        self.videoLayout = QtWidgets.QLabel(self)
        self.videoLayout.setText("")
        self.videoLayout.setMinimumSize(QtCore.QSize(constants.ANALYZEIMAGE_WIDTH, constants.ANALYZEIMAGE_HEIGTH))
        self.videoLayout.setMaximumSize(QtCore.QSize(constants.ANALYZEIMAGE_WIDTH, constants.ANALYZEIMAGE_HEIGTH))
        

    def create_spacer(self):
        self.spacerItem53 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem54 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem55 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem56 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem57 = QtWidgets.QSpacerItem(140, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem58 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem59 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem60 = QtWidgets.QSpacerItem(0, 450, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem61 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem62 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.spacerItem63 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem64 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem65 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)


    def add_items(self):
        self.lyth_headline_Analyze.addWidget(self.lbl_headline_Analyze)
        self.lyth_headline_Analyze.addItem(self.spacerItem53)
        self.lyth_headline_Analyze.addWidget(self.btn_info_Analyze)
        self.verticalLayout_6.addLayout(self.lyth_headline_Analyze)
        self.lyth_smallText_Analyze.addWidget(self.label_Analyze, 0, QtCore.Qt.AlignTop)
        self.lyth_smallText_Analyze.addItem(self.spacerItem54)
        self.lyth_smallText_Analyze.addItem(self.spacerItem55)
        self.lytv_bigCenter_Analyze.addLayout(self.lyth_smallText_Analyze)
        self.lyth_centerBig_Analyze.addItem(self.spacerItem56)
        self.lyth_centerBig_Analyze.addItem(self.spacerItem57)
        # self.lyth_centerBig_Analyze.addWidget(self.graphicsAnalyze)
        self.lyth_centerBig_Analyze.addWidget(self.videoLayout)
        self.lyth_centerBig_Analyze.addItem(self.spacerItem58)
        self.verticalLayout_7.addWidget(self.label_IconTop)
        self.verticalLayout_7.addWidget(self.label_IconMid)
        self.verticalLayout_7.addWidget(self.label_IconBottom)
        self.lyth_centerBig_Analyze.addLayout(self.verticalLayout_7)
        self.lyth_centerBig_Analyze.addItem(self.spacerItem59)
        self.lyth_centerBig_Analyze.addItem(self.spacerItem60)
        self.lytv_bigCenter_Analyze.addLayout(self.lyth_centerBig_Analyze)
        self.lytv_bigCenter_Analyze.addLayout(self.lyth_blwCenter_Analyze)
        self.lytv_bigCenter_Analyze.addItem(self.spacerItem61)
        self.verticalLayout_6.addLayout(self.lytv_bigCenter_Analyze)
        self.lyth_bottom_Analyze.addItem(self.spacerItem62)
        self.lyth_bottom_Analyze.addItem(self.spacerItem63)
        self.lyth_bottom_Analyze.addWidget(self.btn_cancelAnalyze)
        self.lyth_bottom_Analyze.addItem(self.spacerItem64)
        self.lyth_bottom_Analyze.addWidget(self.btn_showResult)
        self.lyth_bottom_Analyze.addItem(self.spacerItem65)
        self.verticalLayout_6.addLayout(self.lyth_bottom_Analyze)

    def changeButtonEnabled(self):
        """
        This method is used for changing the enabled-status of the cancel- and the result button, when the analysis has finished
        """
         
        if self.btn_cancelAnalyze.isEnabled():
            print("CancelBtn deactivated, ResultBtn activated")
            self.btn_showResult.setEnabled(True)
            self.btn_cancelAnalyze.setEnabled(False)
        else:
            print("ResultBtn deactivated, CancelBtn activated")
            self.btn_showResult.setEnabled(False)
            self.btn_cancelAnalyze.setEnabled(True)

    def deleteSignLabel(self):
        self.label_IconBottom.setPixmap(QtGui.QPixmap("None"))
        self.label_IconMid.setPixmap(QtGui.QPixmap("None"))
        self.label_IconTop.setPixmap(QtGui.QPixmap("None"))
        

# Result Screen
class Ui_ResultScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(Ui_ResultScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("ResultScreen")

        self.create_layout()
        self.create_button()
        self.create_label()
        self.create_spacer()
        self.add_items() 

    def create_layout(self):
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.lyth_headline_Result = QtWidgets.QHBoxLayout()
        self.lyth_headline_Result.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_Result.setSpacing(constants.HEADLINE_SPACING)
        self.lyth_headline_Result.setObjectName("lyth_headline_Result")

        self.lyth_smallText_Result = QtWidgets.QHBoxLayout()
        self.lyth_smallText_Result.setContentsMargins(0, 0, -1, -1)
        self.lyth_smallText_Result.setObjectName("lyth_smallText_Result")

        self.lyth_bigGrid_Result = QtWidgets.QHBoxLayout()
        self.lyth_bigGrid_Result.setContentsMargins(0, 9, -1, 20)
        self.lyth_bigGrid_Result.setObjectName("lyth_bigGrid_Result")

        self.scrollArea_Result = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.scrollArea_Result.sizePolicy().hasHeightForWidth())
        self.scrollArea_Result.setSizePolicy(sizePolicy)
        self.scrollArea_Result.setMinimumSize(QtCore.QSize(constants.SCROLLAREA_OUTER_MIN_WIDTH, constants.SCROLLAREA_MIN_HEIGTH))
        self.scrollArea_Result.setMaximumSize(QtCore.QSize(constants.SCROLLAREA_OUTER_MAX_WIDTH, constants.SCROLLAREA_MAX_HEIGTH))
        self.scrollArea_Result.setSizeIncrement(QtCore.QSize(0, 0))
        self.scrollArea_Result.setWidgetResizable(True)
        self.scrollArea_Result.setObjectName("scrollArea_Result")

        self.scrollAreaResult = QtWidgets.QWidget()
        self.scrollAreaResult.setGeometry(QtCore.QRect(0, 0, constants.SCROLLAREA_INNER_WIDTH, 360))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaResult.sizePolicy().hasHeightForWidth())
        self.scrollAreaResult.setSizePolicy(sizePolicy)
        self.scrollAreaResult.setMinimumSize(QtCore.QSize(constants.SCROLLAREA_INNER_WIDTH, constants.SCROLLAREA_MIN_HEIGTH))
        self.scrollAreaResult.setMaximumSize(QtCore.QSize(constants.SCROLLAREA_INNER_WIDTH, constants.SCROLLAREA_MAX_HEIGTH))
        self.scrollAreaResult.setObjectName("scrollAreaResult")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.scrollAreaResult)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.gridLayout_Result = QtWidgets.QGridLayout()
        self.gridLayout_Result.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_Result.setContentsMargins(0, 10, 0, 10)
        self.gridLayout_Result.setSpacing(25)
        self.gridLayout_Result.setObjectName("gridLayout_Result")

        self.lyth_bottom_Result = QtWidgets.QHBoxLayout()
        self.lyth_bottom_Result.setContentsMargins(-1, -1, 2, -1)
        self.lyth_bottom_Result.setObjectName("lyth_bottom_Result")

    def create_button(self):

        self.btn_info_Result = QtWidgets.QPushButton(self)
        self.btn_info_Result.setMinimumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_Result.setMaximumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_Result.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_Result.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_Result.setIcon(icon)
        self.btn_info_Result.setIconSize(QtCore.QSize(constants.INFO_ICON_WIDTH, constants.INFO_ICON_HEIGTH))
        self.btn_info_Result.setObjectName("btn_info_Result")
        self.btn_info_Result.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_endResult = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_endResult.sizePolicy().hasHeightForWidth())
        self.btn_endResult.setSizePolicy(sizePolicy)
        self.btn_endResult.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_endResult.setMaximumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_endResult.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_endResult.setText("Beenden")
        self.btn_endResult.clicked.connect(self.gui.cleanup)


    def create_label(self):

        self.lbl_headline_Result = QtWidgets.QLabel(self)
        self.lbl_headline_Result.setStyleSheet(styles.styleHeadlines)
        self.lbl_headline_Result.setText("Auswertung")
        self.lbl_result = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_result.sizePolicy().hasHeightForWidth())
        self.lbl_result.setSizePolicy(sizePolicy)
        self.lbl_result.setMinimumSize(QtCore.QSize(constants.RESULT_SCREEN_PERCENTAGE_WIDTH, constants.RESULT_SCREEN_PERCENTAGE_HEIGTH))
        self.lbl_result.setMaximumSize(QtCore.QSize(constants.RESULT_SCREEN_PERCENTAGE_WIDTH, constants.RESULT_SCREEN_PERCENTAGE_HEIGTH))
        #self.lbl_result.setStyleSheet()
        self.lbl_result.setText("")
        self.lbl_result.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_result.setObjectName("lbl_result")

    def set_ResultLabel(self):
        if(self.logic.getCompareResult()):        
            percentage = self.logic.startAnalysis()
            if((percentage > 100) or (percentage < 0)):
                print("Calculation resulted in impossible percentage")
                self.lbl_result.setText("")
                self.lbl_result.setStyleSheet(None)
            else:
                if(percentage >= constants.PERCENTAGE_GREEN_TO_YELLOW):
                    print("Showing green percentage label")
                    self.lbl_result.setStyleSheet(styles.stylePercentageGreen)
                elif((percentage < constants.PERCENTAGE_GREEN_TO_YELLOW) and (percentage > constants.PERCENTAGE_YELLOW_TO_RED)):
                    print("Showing yellow percentage label")
                    self.lbl_result.setStyleSheet(styles.stylePercentageYellow)
                elif(percentage < constants.PERCENTAGE_YELLOW_TO_RED):
                    print("Showing red percentage label")
                    self.lbl_result.setStyleSheet(styles.stylePercentageRed)
                
                print("Showing percentage label with " + str(percentage) + "%")
                self.lbl_result.setText(str(percentage)+"%")
        else:
            print("No compareResult calculation necessary")
            self.lbl_result.setText("")
            self.lbl_result.setStyleSheet(None)

    def create_gridContent(self):
        """
        creating the gridContent according to the content of array_dataInput and compareResult
        """
        if(self.logic.getCompareResult()):
            print("Es wird eine Auswertung durchgeführt")
        else:
            print("Die Ergebnisse werden nur angezeigt")

        #Insert header to gridLayout
        row_count = 0
        while(row_count < constants.RESULT_SCREEN_ROWS):
            self.lbl_header_schild = QtWidgets.QLabel(self.scrollAreaResult)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.lbl_header_schild.sizePolicy().hasHeightForWidth())
            self.lbl_header_schild.setSizePolicy(sizePolicy)
            self.lbl_header_schild.setMinimumSize(QtCore.QSize(constants.RESULT_SCREEN_HEADER_WIDTH, constants.RESULT_SCREEN_HEADER_HEIGTH))
            self.lbl_header_schild.setMaximumSize(QtCore.QSize(constants.RESULT_SCREEN_HEADER_WIDTH, constants.RESULT_SCREEN_HEADER_HEIGTH))
            self.lbl_header_schild.setStyleSheet(styles.styleGridHeadline)
            self.lbl_header_schild.setText("Schild")
            #self.lbl_header_schild.setAlignment(QtCore.Qt.AlignCenter)
            self.lbl_header_schild.setObjectName("lbl_header_schild"+str(row_count))
            self.gridLayout_Result.addWidget(self.lbl_header_schild, 0, row_count, 1, 1)

            row_count=row_count+1

            if self.logic.getCompareResult():
                self.lbl_header_eingabe = QtWidgets.QLabel(self.scrollAreaResult)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.lbl_header_eingabe.sizePolicy().hasHeightForWidth())
                self.lbl_header_eingabe.setSizePolicy(sizePolicy)
                self.lbl_header_eingabe.setMinimumSize(QtCore.QSize(constants.RESULT_SCREEN_HEADER_WIDTH, constants.RESULT_SCREEN_HEADER_HEIGTH))
                self.lbl_header_eingabe.setMaximumSize(QtCore.QSize(constants.RESULT_SCREEN_HEADER_WIDTH, constants.RESULT_SCREEN_HEADER_HEIGTH))
                self.lbl_header_eingabe.setStyleSheet(styles.styleGridHeadline)
                self.lbl_header_eingabe.setText("Eingabe")
                #self.lbl_header_eingabe.setAlignment(QtCore.Qt.AlignCenter)
                self.lbl_header_eingabe.setObjectName("lbl_header_eingabe"+str(row_count))
                self.gridLayout_Result.addWidget(self.lbl_header_eingabe, 0, row_count, 1, 1, QtCore.Qt.AlignHCenter)

            row_count=row_count+1

            self.lbl_header_erkannt = QtWidgets.QLabel(self.scrollAreaResult)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.lbl_header_erkannt.sizePolicy().hasHeightForWidth())
            self.lbl_header_erkannt.setSizePolicy(sizePolicy)
            self.lbl_header_erkannt.setMinimumSize(QtCore.QSize(constants.RESULT_SCREEN_HEADER_WIDTH, constants.RESULT_SCREEN_HEADER_HEIGTH))
            self.lbl_header_erkannt.setMaximumSize(QtCore.QSize(constants.RESULT_SCREEN_HEADER_WIDTH, constants.RESULT_SCREEN_HEADER_HEIGTH))
            self.lbl_header_erkannt.setStyleSheet(styles.styleGridHeadline)
            self.lbl_header_erkannt.setText("Erkannt")
            #self.lbl_header_erkannt.setAlignment(QtCore.Qt.AlignCenter)
            self.lbl_header_erkannt.setObjectName("lbl_header_erkannt"+str(row_count))
            self.gridLayout_Result.addWidget(self.lbl_header_erkannt, 0, row_count, 1, 1, QtCore.Qt.AlignHCenter)

            row_count=row_count+1

        #insert data
        line=1
        column=0
        
        for array_count in range(len(self.logic.array_dataInput[constants.DATA_ARRAY_SIGN_ID])):

            self.sign_id = ":/signs/" + str(self.logic.getDataArray(array_count, constants.DATA_ARRAY_SIGN_ID))
            self.sign_input = self.logic.getDataArray(array_count, constants.DATA_ARRAY_SIGN_INPUT)
            self.sign_detected = self.logic.getDataArray(array_count, constants.DATA_ARRAY_SIGN_DETECTED)

            print("SignID: " + str(self.logic.getDataArray(array_count, constants.DATA_ARRAY_SIGN_ID)) + "; Input: " + str(self.sign_input) + "; Detected: " + str(self.sign_detected))

            if (self.sign_detected > 0) or ( (self.logic.getCompareResult() == True) and (self.sign_input > 0) ) :

                self.name_sign = QtWidgets.QLabel(self.scrollAreaResult)
                self.name_sign.setMinimumSize(QtCore.QSize(constants.SIGN_WIDTH, constants.SIGN_HEIGTH))
                self.name_sign.setMaximumSize(QtCore.QSize(constants.SIGN_WIDTH, constants.SIGN_HEIGTH))
                self.name_sign.setPixmap(QtGui.QPixmap(self.sign_id))
                self.name_sign.setScaledContents(True)
                self.gridLayout_Result.addWidget(self.name_sign, line,column,1,1)

                column = column+1

                if self.logic.getCompareResult():
                    self.lbl_eingabe = QtWidgets.QLabel(self.scrollAreaResult)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_eingabe.sizePolicy().hasHeightForWidth())
                    self.lbl_eingabe.setSizePolicy(sizePolicy)
                    self.lbl_eingabe.setMinimumSize(QtCore.QSize(constants.SIGN_COUNT_WIDTH, constants.SIGN_COUNT_HEIGTH))
                    self.lbl_eingabe.setMaximumSize(QtCore.QSize(constants.SIGN_COUNT_WIDTH, constants.SIGN_COUNT_HEIGTH))
                    self.lbl_eingabe.setObjectName("lbl_eingabe")
                    self.lbl_eingabe.setStyleSheet(styles.styleResultLabel)
                    self.lbl_eingabe.setText(str(self.sign_input))
                    self.gridLayout_Result.addWidget(self.lbl_eingabe, line,column,1,1, QtCore.Qt.AlignHCenter)
                column = column+1

                self.lbl_erkannt = QtWidgets.QLabel(self.scrollAreaResult)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.lbl_erkannt.sizePolicy().hasHeightForWidth())
                self.lbl_erkannt.setSizePolicy(sizePolicy)
                self.lbl_erkannt.setMinimumSize(QtCore.QSize(constants.SIGN_COUNT_WIDTH, constants.SIGN_COUNT_HEIGTH))
                self.lbl_erkannt.setMaximumSize(QtCore.QSize(constants.SIGN_COUNT_WIDTH, constants.SIGN_COUNT_HEIGTH))
                self.lbl_erkannt.setObjectName("lbl_erkannt")
                self.lbl_erkannt.setStyleSheet(styles.styleResultLabel)
                self.lbl_erkannt.setText(str(self.sign_detected))
                self.gridLayout_Result.addWidget(self.lbl_erkannt, line,column,1,1, QtCore.Qt.AlignHCenter)

                column = column+1

            if column >= constants.RESULT_SCREEN_ROWS:
                column = 0
                line = line+1
             
    def create_spacer(self):
        self.spacerItem66 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem67 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem68 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem69 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.spacerItem70 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem71 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem72 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.spacerItem73 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem74 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def add_items(self):
        self.lyth_headline_Result.addWidget(self.lbl_headline_Result)
        self.lyth_headline_Result.addItem(self.spacerItem66)
        self.lyth_headline_Result.addWidget(self.btn_info_Result)
        self.verticalLayout_9.addLayout(self.lyth_headline_Result)
        self.lyth_smallText_Result.addItem(self.spacerItem67)
        self.lyth_smallText_Result.addWidget(self.lbl_result, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.lyth_smallText_Result.addItem(self.spacerItem68)
        self.lyth_smallText_Result.addItem(self.spacerItem69)
        self.verticalLayout_9.addLayout(self.lyth_smallText_Result)
        self.lyth_bigGrid_Result.addItem(self.spacerItem70)
        self.horizontalLayout_5.addLayout(self.gridLayout_Result)
        self.scrollArea_Result.setWidget(self.scrollAreaResult)
        self.lyth_bigGrid_Result.addWidget(self.scrollArea_Result)
        self.lyth_bigGrid_Result.addItem(self.spacerItem71)
        self.verticalLayout_9.addLayout(self.lyth_bigGrid_Result)
        self.lyth_bottom_Result.addItem(self.spacerItem72)
        self.lyth_bottom_Result.addItem(self.spacerItem73)   
        self.lyth_bottom_Result.addWidget(self.btn_endResult)
        self.lyth_bottom_Result.addItem(self.spacerItem74)
        self.verticalLayout_9.addLayout(self.lyth_bottom_Result)

    def delete_grid(self):
        if self.gridLayout_Result.itemAt(0) is None:
            print("ResultGrid is empty")
        else:
            #print("not empty")
            item_count=self.gridLayout_Result.count()
            item_counter = item_count-1
            while(item_counter >= 0):
                #print("removing item " + str(item_counter))
                item = self.gridLayout_Result.itemAt(item_counter)
                #Unschön, aber notwendig, da sonst letztes Element immer angezeigt wird.
                widget = item.widget()
                widget.setText("")
                widget.setPixmap(QtGui.QPixmap("None"))
                #Löschen des Elementes aus dem GridLayout
                self.gridLayout_Result.removeItem(item)
                item_counter=item_counter-1  

       
# Demo Data Screen
class Ui_DemoDataScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(Ui_DemoDataScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("DemoDataScreen")

        self.create_layout()
        self.create_button()
        self.create_label()
        self.create_spacer()
        self.add_items()        


    def create_layout(self):
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.lyth_headline_DemoData = QtWidgets.QHBoxLayout()
        self.lyth_headline_DemoData.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_DemoData.setSpacing(constants.HEADLINE_SPACING)
        self.lyth_headline_DemoData.setObjectName("lyth_headline_DemoData")

        self.lyth_smallText_DemoData = QtWidgets.QHBoxLayout()
        self.lyth_smallText_DemoData.setContentsMargins(20, 0, -1, -1)
        self.lyth_smallText_DemoData.setObjectName("lyth_smallText_DemoData")

        self.lyth_bigGrid_DemoData = QtWidgets.QHBoxLayout()
        self.lyth_bigGrid_DemoData.setContentsMargins(0, 9, -1, 20)
        self.lyth_bigGrid_DemoData.setObjectName("lyth_bigGrid_DemoData")

        self.scrollArea_DemoData = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.scrollArea_DemoData.sizePolicy().hasHeightForWidth())
        self.scrollArea_DemoData.setSizePolicy(sizePolicy)
        self.scrollArea_DemoData.setMinimumSize(QtCore.QSize(constants.SCROLLAREA_OUTER_MIN_WIDTH, constants.SCROLLAREA_MIN_HEIGTH))
        self.scrollArea_DemoData.setMaximumSize(QtCore.QSize(constants.SCROLLAREA_OUTER_MAX_WIDTH, constants.SCROLLAREA_MAX_HEIGTH))
        self.scrollArea_DemoData.setSizeIncrement(QtCore.QSize(0, 0))
        self.scrollArea_DemoData.setWidgetResizable(True)
        self.scrollArea_DemoData.setObjectName("scrollArea_DemoData")
        self.scrollAreaWidget_DemoData = QtWidgets.QWidget()
        self.scrollAreaWidget_DemoData.setGeometry(QtCore.QRect(0, 0, constants.SCROLLAREA_INNER_WIDTH, 597))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidget_DemoData.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidget_DemoData.setSizePolicy(sizePolicy)
        self.scrollAreaWidget_DemoData.setMinimumSize(QtCore.QSize(constants.SCROLLAREA_INNER_WIDTH, constants.SCROLLAREA_MIN_HEIGTH))
        self.scrollAreaWidget_DemoData.setMaximumSize(QtCore.QSize(constants.SCROLLAREA_INNER_WIDTH, constants.SCROLLAREA_MAX_HEIGTH))
        self.scrollAreaWidget_DemoData.setObjectName("scrollAreaWidget_DemoData")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.scrollAreaWidget_DemoData)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout_DemoData = QtWidgets.QGridLayout()
        self.gridLayout_DemoData.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_DemoData.setContentsMargins(0, 10, 0, 10)
        self.gridLayout_DemoData.setHorizontalSpacing(40)
        self.gridLayout_DemoData.setVerticalSpacing(25)
        self.gridLayout_DemoData.setObjectName("gridLayout_DemoData")

        self.lyth_bottom_DemoData = QtWidgets.QHBoxLayout()
        self.lyth_bottom_DemoData.setContentsMargins(-1, -1, 0, -1)
        self.lyth_bottom_DemoData.setSpacing(constants.HEADLINE_SPACING)
        self.lyth_bottom_DemoData.setObjectName("lyth_bottom_DemoData")


    def create_button(self):
        self.btn_info_DemoData = QtWidgets.QPushButton(self)
        self.btn_info_DemoData.setMinimumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_DemoData.setMaximumSize(QtCore.QSize(constants.INFO_BUTTON_WIDTH, constants.INFO_BUTTON_HEIGTH))
        self.btn_info_DemoData.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_DemoData.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_DemoData.setIcon(icon)
        self.btn_info_DemoData.setIconSize(QtCore.QSize(constants.INFO_ICON_WIDTH, constants.INFO_ICON_HEIGTH))
        self.btn_info_DemoData.setObjectName("btn_info_DemoData")
        self.btn_info_DemoData.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_ok_demoData = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_ok_demoData.sizePolicy().hasHeightForWidth())
        self.btn_ok_demoData.setSizePolicy(sizePolicy)
        self.btn_ok_demoData.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_ok_demoData.setMaximumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_ok_demoData.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_ok_demoData.setText("OK")
        self.btn_ok_demoData.setCheckable(False)
        self.btn_ok_demoData.setFlat(False)
        self.btn_ok_demoData.setObjectName("btn_ok_demoData")
        self.btn_ok_demoData.clicked.connect(lambda: self.gui.change_screen_back())


    def create_label(self):
        self.lbl_headline_DemoData = QtWidgets.QLabel(self)
        self.lbl_headline_DemoData.setStyleSheet(styles.styleHeadlines)
        self.lbl_headline_DemoData.setText("Demo")
        self.lbl_headline_DemoData.setObjectName("lbl_headline_DemoData")
        self.label_DIScreen_DemoData = QtWidgets.QLabel(self)
        self.label_DIScreen_DemoData.setStyleSheet(styles.styleText1)
        self.label_DIScreen_DemoData.setText("Anzahl der Schilder im Video")
        self.label_DIScreen_DemoData.setObjectName("label_DIScreen_DemoData")


    def create_spacer(self):
        self.spacerItem75 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem76 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem77 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.spacerItem78 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem79 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem80 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.spacerItem81 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem82 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)


    def create_grid(self, filepath):

        row_counter = 0
        col_counter = 0
        
        with open(filepath, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            
            next(csv_reader)

            for line in csv_reader:
                if int(line[constants.DEMODATA_CSV_SIGN_COUNT]) > 0:

                    self.sign_id = ":/signs/" + line[constants.DEMODATA_CSV_SIGN_ID]
                    self.sign_count = line[constants.DEMODATA_CSV_SIGN_COUNT]

                    self.name_sign = QtWidgets.QLabel(self.scrollAreaWidget_DemoData)
                    self.name_sign.setMinimumSize(QtCore.QSize(constants.SIGN_WIDTH, constants.SIGN_HEIGTH))
                    self.name_sign.setMaximumSize(QtCore.QSize(constants.SIGN_WIDTH, constants.SIGN_HEIGTH))
                    self.name_sign.setPixmap(QtGui.QPixmap(self.sign_id))
                    self.name_sign.setScaledContents(True)
                    self.gridLayout_DemoData.addWidget(self.name_sign, row_counter,col_counter,1,1)

                    col_counter = col_counter+1

                    self.lbl_amount = QtWidgets.QLabel(self.scrollAreaWidget_DemoData)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_amount.sizePolicy().hasHeightForWidth())
                    self.lbl_amount.setSizePolicy(sizePolicy)
                    self.lbl_amount.setMinimumSize(QtCore.QSize(constants.SIGN_COUNT_WIDTH, constants.SIGN_COUNT_HEIGTH))
                    self.lbl_amount.setMaximumSize(QtCore.QSize(constants.SIGN_COUNT_WIDTH, constants.SIGN_COUNT_HEIGTH))
                    self.lbl_amount.setObjectName("lbl_amount")
                    self.lbl_amount.setStyleSheet(styles.styleText1)
                    self.lbl_amount.setText(self.sign_count)
                    self.gridLayout_DemoData.addWidget(self.lbl_amount, row_counter, col_counter, 1, 1)

                    col_counter = col_counter+1
                    if(col_counter > constants.DISCREEN_COLUMNS):
                        col_counter = 0
                        row_counter = row_counter+1

        csvfile.close()

    def delete_grid(self):
        
   
        if self.gridLayout_DemoData.itemAt(0) is None:
            print("DemoData-Grid is empty")
        else:
            #print("not empty")
            count=self.gridLayout_DemoData.count()
            item_count = count-1
            while(item_count >= 0):
                #print("removing item " + str(item_count))
                item = self.gridLayout_DemoData.itemAt(item_count)
                #Unschön, aber notwendig, da sonst letztes Element immer angezeigt wird.
                widget = item.widget()
                widget.setText("")
                widget.setPixmap(QtGui.QPixmap("None"))
                #Löschen des Elementes aus dem GridLayout
                self.gridLayout_DemoData.removeItem(item)
                item_count=item_count-1       


    def add_items(self):
        self.lyth_headline_DemoData.addWidget(self.lbl_headline_DemoData)
        self.lyth_headline_DemoData.addItem(self.spacerItem75)
        self.lyth_headline_DemoData.addWidget(self.btn_info_DemoData)
        self.verticalLayout_8.addLayout(self.lyth_headline_DemoData)
        self.lyth_smallText_DemoData.addWidget(self.label_DIScreen_DemoData, 0, QtCore.Qt.AlignTop)
        self.lyth_smallText_DemoData.addItem(self.spacerItem76)
        self.lyth_smallText_DemoData.addItem(self.spacerItem77)
        self.verticalLayout_8.addLayout(self.lyth_smallText_DemoData)
        self.lyth_bigGrid_DemoData.addItem(self.spacerItem78)
        self.horizontalLayout_4.addLayout(self.gridLayout_DemoData)
        self.scrollArea_DemoData.setWidget(self.scrollAreaWidget_DemoData)
        self.lyth_bigGrid_DemoData.addWidget(self.scrollArea_DemoData)
        self.lyth_bigGrid_DemoData.addItem(self.spacerItem79)
        self.verticalLayout_8.addLayout(self.lyth_bigGrid_DemoData)
        self.lyth_bottom_DemoData.addItem(self.spacerItem80)
        self.lyth_bottom_DemoData.addItem(self.spacerItem81)
        self.lyth_bottom_DemoData.addWidget(self.btn_ok_demoData)
        self.lyth_bottom_DemoData.addItem(self.spacerItem82)
        self.verticalLayout_8.addLayout(self.lyth_bottom_DemoData)


# Info Screen
class Ui_InfoScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(Ui_InfoScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("InfoScreen")
        self.setFixedSize( self.gui.size.width() * constants.INFOSCREEN_SIZE_RATIO, self.gui.size.height() * constants.INFOSCREEN_SIZE_RATIO)
        self.setStyleSheet(styles.styleBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        self.create_layout()
        self.create_button()
        self.create_label()
        self.create_spacer()
        self.add_items()        

    def create_layout(self):
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.lyth_headline_Info = QtWidgets.QHBoxLayout()
        self.lyth_headline_Info.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_Info.setSpacing(constants.HEADLINE_SPACING)
        self.lyth_headline_Info.setObjectName("lyth_headline_Info")
        self.lbl_headline_Info = QtWidgets.QLabel(self)

        self.verticalLayout_12.addLayout(self.lyth_headline_Info)
        self.lytv_centerInfo = QtWidgets.QVBoxLayout()
        self.lytv_centerInfo.setContentsMargins(-1, 45, -1, -1)
        self.lytv_centerInfo.setSpacing(20)
        self.lytv_centerInfo.setObjectName("lytv_centerInfo")

        self.lyth_bottom_Info = QtWidgets.QHBoxLayout()
        self.lyth_bottom_Info.setContentsMargins(-1, -1, 2, -1)
        self.lyth_bottom_Info.setObjectName("lyth_bottom_Info")

    def create_button(self):
        self.btn_closeInfo = QtWidgets.QPushButton(self)
        self.btn_closeInfo.setMinimumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_closeInfo.setMaximumSize(QtCore.QSize(constants.BLUEBUTTONSMALL_WIDTH, constants.BLUEBUTTONSMALL_HEIGTH))
        self.btn_closeInfo.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_closeInfo.setText("OK")
        self.btn_closeInfo.setCheckable(False)
        self.btn_closeInfo.setFlat(False)
        self.btn_closeInfo.setObjectName("btn_closeInfo")
        self.btn_closeInfo.clicked.connect(lambda: self.hide())

    def create_label(self):
        self.lbl_headline_Info.setStyleSheet(styles.styleHeadlines)
        self.lbl_headline_Info.setText("Über Schilder Kröten")
        self.lbl_headline_Info.setObjectName("lbl_headline_Info")

        self.label_Logo = QtWidgets.QLabel(self)
        self.label_Logo.setMinimumSize(QtCore.QSize(500, 0))
        self.label_Logo.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_Logo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Logo.setPixmap(QtGui.QPixmap(":/icons/logoSK_big_1"))
        self.label_Logo.setObjectName("label_Logo")

        self.label_infoText = QtWidgets.QLabel(self)
        self.label_infoText.setStyleSheet(styles.styleText1)      
        self.label_infoText.setText("Schilder Kröten GmbH\n""Musterstraße 1\n""12345 Musterstadt\n""\n""Ansprechpartner:\n""Herr Mayer\n""\n""0123-456789\n""")
        self.label_infoText.setAlignment(QtCore.Qt.AlignCenter)
        self.label_infoText.setObjectName("label_infoText")

    def create_spacer(self):
        self.spacerItem83 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem84 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spacerItem85 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.spacerItem86 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem87 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def add_items(self):
        self.lyth_headline_Info.addWidget(self.lbl_headline_Info)
        self.lyth_headline_Info.addItem(self.spacerItem83)
        self.lytv_centerInfo.addWidget(self.label_Logo)
        self.lytv_centerInfo.addWidget(self.label_infoText)
        self.lytv_centerInfo.addItem(self.spacerItem84)
        self.verticalLayout_12.addLayout(self.lytv_centerInfo)
        self.lyth_bottom_Info.addItem(self.spacerItem85)
        self.lyth_bottom_Info.addItem(self.spacerItem86)
        self.lyth_bottom_Info.addWidget(self.btn_closeInfo)
        self.lyth_bottom_Info.addItem(self.spacerItem87)
        self.verticalLayout_12.addLayout(self.lyth_bottom_Info)
