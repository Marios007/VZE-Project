from PyQt5 import QtCore, QtGui, QtWidgets
import gui.styles as styles
import gui.image_ressources as image_ressources
import csv


class VzeGui(QtWidgets.QMainWindow):

    stack_lastScreen = []
    array_dataInput = [[0 for x in range(43)] for y in range(2)]
    demo_video1 = "./gui/pics/DemoVideos/DemoVideo_gutesWetter.mp4"
    demo_video1_preview = "./gui/pics/DemoVideos/DemoVideo_gutesWetter_Thumbnail.jpg"
    demo_video2 = "./gui/pics/DemoVideos/DemoVideo_schlechtesWetter.mp4"
    demo_video2_preview = "./gui/pics/DemoVideos/DemoVideo_schlechtesWetter_Thumbnail.jpg"

    def __init__(self, logicInterface):
        QtWidgets.QMainWindow.__init__(self)
        print ("loading UI")
       
        self.logic = logicInterface

        # Setting Window Title and Icon
        self.setWindowTitle("VerkehrsZeichenErkennung VZE")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/logo_schild"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
    
       # Size of window is always 0,65 times of availabe window
        size = QtWidgets.QDesktopWidget().availableGeometry()
        self.setMinimumSize( size.width() * 0.65, size.height() * 0.65)

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
        #define startscreen
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(window)

    def build_screens(self):

        #Build UI with each screen
        print ("Build screens")
        #0
        self.startscreen = ui_startscreen(self.logic, self)
        self.stackedWidget.addWidget(self.startscreen)
        #1
        self.demoscreen = ui_demoscreen(self.logic, self)
        self.stackedWidget.addWidget(self.demoscreen)
        #2
        self.previewscreen = ui_previewscreen(self.logic, self)
        self.stackedWidget.addWidget(self.previewscreen)
        #3
        self.diScreen = ui_DIScreen(self.logic, self)
        self.stackedWidget.addWidget(self.diScreen)
        #4
        self.analyzepvscreen = ui_analyzePvScreen(self.logic, self)
        self.stackedWidget.addWidget(self.analyzepvscreen)
        #5
        self.analyzescreen = ui_analyzeScreen(self.logic, self)
        self.stackedWidget.addWidget(self.analyzescreen)
        #6
        self.demodatascreen = ui_DemoDataScreen(self.logic, self)
        self.stackedWidget.addWidget(self.demodatascreen)
        #7
        self.resultscreen = ui_ResultScreen(self.logic, self)
        self.stackedWidget.addWidget(self.resultscreen)
        #8
        self.infoscreen = ui_InfoScreen(self.logic, self)

        self.verticalLayout.addWidget(self.stackedWidget)
         
     #    


    #change to next screen and save last screen to stack
    def change_screen(self, nextScreen):
        self.set_lastScreen()
        self.stackedWidget.setCurrentIndex(nextScreen)
        return

    # save last screen on stack
    def set_lastScreen(self):
        self.stack_lastScreen.append(self.stackedWidget.currentIndex())
        print("Save last screen: " + str(self.stackedWidget.currentIndex()))

    # go back  to last screen and remove first value from stack
    def change_screen_back(self):
        print("print stack: " + str(self.stack_lastScreen))
        self.stackedWidget.setCurrentIndex(self.stack_lastScreen.pop())
        return 

    def create_DemoDataGrid(self, demoID):
        print("loading demo data grid for demovideo " + str(demoID))

        demodatafile=""

        if(demoID == 1):
            demodatafile='./gui/demo_data_1.csv'
        elif (demoID == 2):
            demodatafile='./gui/demo_data_2_full.csv'
        else:
            print("Unknown error")

        self.demodatascreen.delete_grid()
        self.demodatascreen.create_grid(demodatafile)
        self.change_screen(6)

    def showPreviewImage(self, filepath, nextScreen):
        print("method showPreviewImage")
        #file = self.logic.getFilePath()
        #print(filepath)
                
        #if image file
        if((filepath.endswith('.jpg')) or (filepath.endswith('.jpeg')) or (filepath.endswith('.gif')) or (filepath.endswith('.png')) or (filepath.endswith('.bmp'))):
            print("File is an image") 


        #if video file
        elif((filepath.endswith('.avi')) or (filepath.endswith('.mov')) or (filepath.endswith('.mp4')) or (filepath.endswith('.mpeg'))):
            print("File is a video")
            #Create Thumbnail of video
            #cap = cv2.VideoCapture(filepath)
            #success, image = cap.read()
            #print(success)
            #cv2.imwrite("./gui/pics/thumb.jpg", image)
            #thumb = cv2.resize(image, 790, interpolation=cv2.INTER_AREA)
            #filepath = "./gui/pics/thumb.jpg"


        else:
            print("Unsupported FileType")

        pixmap = QtGui.QPixmap(filepath)
        pixmap_scaled = pixmap.scaled(790, 410)
        graphicsScene = QtWidgets.QGraphicsScene(self)
        graphicsScene.addPixmap(pixmap_scaled)

        if(nextScreen == 2):
            self.previewscreen.graphicsPreview.setScene(graphicsScene)
        elif(nextScreen == 4):
            self.analyzepvscreen.graphicsAnalyzePreview.setScene(graphicsScene)
        
        self.change_screen(nextScreen)



# Start Screen
class ui_startscreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_startscreen, self).__init__()

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
        self.btn_info_startscreen.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_startscreen.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_startscreen.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_startscreen.setIcon(icon)
        self.btn_info_startscreen.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_startscreen.setObjectName("btn_info_startscreen")
        self.btn_info_startscreen.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_loadFile = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_loadFile.sizePolicy().hasHeightForWidth())
        self.btn_loadFile.setSizePolicy(sizePolicy)
        self.btn_loadFile.setMinimumSize(QtCore.QSize(350, 220))
        self.btn_loadFile.setStyleSheet(styles.styleBluebuttonbig)
        self.btn_loadFile.setText(("Datei auswählen"))
        self.btn_loadFile.setToolTip('Laden eines Videos oder Bildes')
        self.btn_loadFile.clicked.connect(self.logic.loadFile)
        self.btn_loadFile.clicked.connect(lambda: self.gui.showPreviewImage(self.logic.getFilePath(),2))


        self.btn_demoToDemo = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_demoToDemo.sizePolicy().hasHeightForWidth())
        self.btn_demoToDemo.setSizePolicy(sizePolicy)
        self.btn_demoToDemo.setMinimumSize(QtCore.QSize(350, 220))
        self.btn_demoToDemo.setStyleSheet(styles.styleBluebuttonbig)
        self.btn_demoToDemo.setText(("Demo auswählen"))
        self.btn_demoToDemo.setToolTip('Demo Videos wählen')
        self.btn_demoToDemo.clicked.connect(lambda: self.gui.change_screen(1))
    
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
class ui_demoscreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_demoscreen, self).__init__()

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
        self.lyth_headline_demoscreen.setSpacing(6)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_demoscreen.sizePolicy().hasHeightForWidth())
        self.btn_info_demoscreen.setSizePolicy(sizePolicy)
        self.btn_info_demoscreen.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_demoscreen.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_demoscreen.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_demoscreen.setIcon(icon)
        self.btn_info_demoscreen.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_demoscreen.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_demoSonne = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_demoSonne.sizePolicy().hasHeightForWidth())
        self.btn_demoSonne.setSizePolicy(sizePolicy)
        self.btn_demoSonne.setMinimumSize(QtCore.QSize(350, 220))
        self.btn_demoSonne.setStyleSheet(styles.styleBluebuttonbig)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/demo_sonne"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_demoSonne.setIcon(icon)
        self.btn_demoSonne.setIconSize(QtCore.QSize(30, 30))
        self.btn_demoSonne.setText(("Video mit Sonne"))
        self.btn_demoSonne.clicked.connect(lambda: self.logic.setFilePath(self.gui.demo_video1))
        #self.btn_demoSonne.clicked.connect(lambda: self.gui.showPreviewImage(self.logic.getFilePath(),4))
        #Temporär den Screenshot des Videos verwenden, bis selbst erstellt werden kann
        self.btn_demoSonne.clicked.connect(lambda: self.gui.showPreviewImage(self.gui.demo_video1_preview,4))
        
        self.btn_demoRegen = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_demoRegen.sizePolicy().hasHeightForWidth())
        self.btn_demoRegen.setSizePolicy(sizePolicy)
        self.btn_demoRegen.setMinimumSize(QtCore.QSize(350, 220))
        self.btn_demoRegen.setStyleSheet(styles.styleBluebuttonbig)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/demo_regen"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_demoRegen.setIcon(icon)
        self.btn_demoRegen.setIconSize(QtCore.QSize(30, 30))
        self.btn_demoRegen.setText(("Video mit Regen"))
        self.btn_demoRegen.clicked.connect(lambda: self.logic.setFilePath(self.gui.demo_video2))
        #self.btn_demoRegen.clicked.connect(lambda: self.gui.showPreviewImage(self.logic.getFilePath(),4))
        #Temporär den Screenshot des Videos verwenden, bis selbst erstellt werden kann
        self.btn_demoRegen.clicked.connect(lambda: self.gui.showPreviewImage(self.gui.demo_video2_preview,4))

        self.btn_dataSonne = QtWidgets.QPushButton(self)
        self.btn_dataSonne.setMinimumSize(QtCore.QSize(55, 55))
        self.btn_dataSonne.setMaximumSize(QtCore.QSize(55, 55))
        self.btn_dataSonne.setStyleSheet(styles.styleSmallButton)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/data_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_dataSonne.setIcon(icon1)
        self.btn_dataSonne.setIconSize(QtCore.QSize(55, 55))
        #self.btn_dataSonne.clicked.connect(lambda: self.gui.change_screen(6))
        self.btn_dataSonne.clicked.connect(lambda: self.gui.create_DemoDataGrid(1))

        self.btn_dataRegen = QtWidgets.QPushButton(self)
        self.btn_dataRegen.setMinimumSize(QtCore.QSize(55, 55))
        self.btn_dataRegen.setMaximumSize(QtCore.QSize(55, 55))
        self.btn_dataRegen.setStyleSheet(styles.styleSmallButton)
        self.btn_dataRegen.setIcon(icon1)
        self.btn_dataRegen.setIconSize(QtCore.QSize(55, 55))
        #self.btn_dataRegen.clicked.connect(lambda: self.gui.change_screen(6))
        self.btn_dataRegen.clicked.connect(lambda: self.gui.create_DemoDataGrid(2))

        self.btn_back_demoscreen = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_back_demoscreen.sizePolicy().hasHeightForWidth())
        self.btn_back_demoscreen.setSizePolicy(sizePolicy)
        self.btn_back_demoscreen.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_back_demoscreen.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_back_demoscreen.setStyleSheet(styles.styleSmallButton)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/back_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_demoscreen.setIcon(icon2)
        self.btn_back_demoscreen.setIconSize(QtCore.QSize(20, 20))
        self.btn_back_demoscreen.clicked.connect(lambda: self.gui.change_screen_back())  
    
    def create_label(self):
        
        self.lbl_demo = QtWidgets.QLabel(self)
        self.lbl_demo.setStyleSheet(styles.styleHeadlines)
        self.lbl_demo.setObjectName("lbl_demo")
        self.lbl_demo.setText(("Demo"))

        self.label_demotext = QtWidgets.QLabel(self)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.label_demotext.sizePolicy().hasHeightForWidth())
        #self.label_demotext.setSizePolicy(sizePolicy)
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

        # Button Info Demoscreen

        
        # Layout big center
        # Label Text and spacer
        # Layout big in big center layout with the 2 buttons
        # Button Back in Demoscreen
        # Set texts
        # Button handler with interface
        

# Preview Screen
class ui_previewscreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_previewscreen, self).__init__()

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
        self.lyth_headline_previewScreen.setSpacing(6)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_previewScreen.sizePolicy().hasHeightForWidth())
        self.btn_info_previewScreen.setSizePolicy(sizePolicy)
        self.btn_info_previewScreen.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_previewScreen.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_previewScreen.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_previewScreen.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_previewScreen.setIcon(icon)
        self.btn_info_previewScreen.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_previewScreen.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_back_previewScreen = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_back_previewScreen.sizePolicy().hasHeightForWidth())
        self.btn_back_previewScreen.setSizePolicy(sizePolicy)
        self.btn_back_previewScreen.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_back_previewScreen.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_back_previewScreen.setStyleSheet(styles.styleSmallButton)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/back_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_previewScreen.setIcon(icon2)
        self.btn_back_previewScreen.setIconSize(QtCore.QSize(20, 20))
        self.btn_back_previewScreen.setObjectName("btn_back_previewScreen")
        self.btn_back_previewScreen.clicked.connect(lambda: self.gui.change_screen_back())

        self.btn_next_preview = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_next_preview.sizePolicy().hasHeightForWidth())
        self.btn_next_preview.setSizePolicy(sizePolicy)
        self.btn_next_preview.setMinimumSize(QtCore.QSize(200, 40))
        self.btn_next_preview.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_next_preview.setCheckable(False)
        self.btn_next_preview.setFlat(False)
        self.btn_next_preview.setText("Weiter")
        self.btn_next_preview.clicked.connect(lambda: self.gui.change_screen(3))

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
        self.graphicsPreview = QtWidgets.QGraphicsView(self)
        self.graphicsPreview.setMinimumSize(QtCore.QSize(800, 420))
        self.graphicsPreview.setMaximumSize(QtCore.QSize(800, 420))
        self.graphicsPreview.setObjectName("graphicsPreview")

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
        self.lyth_centerBig.addWidget(self.graphicsPreview)
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
class ui_DIScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_DIScreen, self).__init__()

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
        self.lyth_headline_DIScreen.setSpacing(6)
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
        self.scrollArea_DIScreen.setMinimumSize(QtCore.QSize(976, 0))
        self.scrollArea_DIScreen.setMaximumSize(QtCore.QSize(1020, 16777215))
        self.scrollArea_DIScreen.setSizeIncrement(QtCore.QSize(0, 0))
        self.scrollArea_DIScreen.setWidgetResizable(True)
        self.scrollArea_DIScreen.setObjectName("scrollArea_DIScreen")

        self.scrollAreaWidget_DIScreen = QtWidgets.QWidget()
        self.scrollAreaWidget_DIScreen.setGeometry(QtCore.QRect(0, 0, 950, 816))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidget_DIScreen.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidget_DIScreen.setSizePolicy(sizePolicy)
        self.scrollAreaWidget_DIScreen.setMinimumSize(QtCore.QSize(950, 0))
        self.scrollAreaWidget_DIScreen.setMaximumSize(QtCore.QSize(950, 16777215))
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_DIScreen.sizePolicy().hasHeightForWidth())
        self.btn_info_DIScreen.setSizePolicy(sizePolicy)
        self.btn_info_DIScreen.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_DIScreen.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_DIScreen.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_DIScreen.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_DIScreen.setIcon(icon)
        self.btn_info_DIScreen.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_DIScreen.setObjectName("btn_info_DIScreen")
        self.btn_info_DIScreen.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_back_DI = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_back_DI.sizePolicy().hasHeightForWidth())
        self.btn_back_DI.setSizePolicy(sizePolicy)
        self.btn_back_DI.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_back_DI.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_back_DI.setStyleSheet(styles.styleSmallButton)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/back_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_DI.setIcon(icon2)
        self.btn_back_DI.setIconSize(QtCore.QSize(20, 20))
        self.btn_back_DI.setCheckable(True)
        self.btn_back_DI.setObjectName("btn_back_DI")
        self.btn_back_DI.clicked.connect(lambda: self.gui.change_screen_back())

        self.btn_reset = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_reset.sizePolicy().hasHeightForWidth())
        self.btn_reset.setSizePolicy(sizePolicy)
        self.btn_reset.setMinimumSize(QtCore.QSize(220, 40))
        self.btn_reset.setMaximumSize(QtCore.QSize(220, 40))
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
        self.btn_skip.setMinimumSize(QtCore.QSize(220, 40))
        self.btn_skip.setMaximumSize(QtCore.QSize(220, 40))
        self.btn_skip.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_skip.setText("Überspringen")
        self.btn_skip.setCheckable(False)
        self.btn_skip.setFlat(False)
        self.btn_skip.setObjectName("btn_skip")
        #self.btn_skip.clicked.connect(lambda: self.gui.change_screen(4))
        self.btn_skip.clicked.connect(lambda: self.gui.showPreviewImage(self.logic.getFilePath(),4))

        self.btn_DInext = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_DInext.sizePolicy().hasHeightForWidth())
        self.btn_DInext.setSizePolicy(sizePolicy)
        self.btn_DInext.setMinimumSize(QtCore.QSize(220, 40))
        self.btn_DInext.setMaximumSize(QtCore.QSize(220, 40))
        self.btn_DInext.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_DInext.setText("Weiter")
        self.btn_DInext.setCheckable(False)
        self.btn_DInext.setFlat(False)
        self.btn_DInext.setObjectName("btn_DInext")
        self.btn_DInext.clicked.connect(lambda: self.save_gridContent())
        self.btn_DInext.clicked.connect(lambda: self.gui.showPreviewImage(self.logic.getFilePath(),4))

    def create_label(self):
        self.lbl_headline_DIScreen = QtWidgets.QLabel(self)
        self.lbl_headline_DIScreen.setStyleSheet(styles.styleHeadlines)
        self.lbl_headline_DIScreen.setText("Datei Analyse")
        self.lbl_headline_DIScreen.setObjectName("lbl_headline_DIScreen")

        self.label_DIScreen_smalltext = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_DIScreen_smalltext.sizePolicy().hasHeightForWidth())
        self.label_DIScreen_smalltext.setSizePolicy(sizePolicy)
        self.label_DIScreen_smalltext.setStyleSheet(styles.styleText1)
        self.label_DIScreen_smalltext.setText("Anzahl der Schilder eingeben (Optional)")
        self.label_DIScreen_smalltext.setObjectName("label_DIScreen_smalltext")
    
    def create_gridContent(self):

        i = 0
        j = 0
        k = 0
        
        while (i <= 10):    
            while (j <= 7):
                if(k<43):
                    #print("sign: i:"+ str(i) + " j:"+ str(j) + " k:"+ str(k))
                    #create signs
                    self.name_sign = "lbl_sign_"+ str(k)
                    self.sign_id = ":/signs/" + str(k)
                    self.name_sign = QtWidgets.QLabel(self.scrollAreaWidget_DIScreen)
                    self.name_sign.setMinimumSize(QtCore.QSize(48, 48))
                    self.name_sign.setMaximumSize(QtCore.QSize(48, 48))
                    self.name_sign.setObjectName("lbl_sign_"+ str(k))
                    self.name_sign.setPixmap(QtGui.QPixmap(self.sign_id))
                    self.name_sign.setScaledContents(True)

                    self.gridLayout_DIScreen.addWidget(self.name_sign, i,j,1,1)
                    
                    #j++ to create the spinbox next to sign (label)
                    j =j+1

                    # create spinboxes 

                    # print("sb: i:"+ str(i) + " j:"+ str(j) + " k:"+ str(k))
                    self.name_sb = "spinBox_"+ str(k)
                    self.name_sb = QtWidgets.QSpinBox(self.scrollAreaWidget_DIScreen)
                    self.name_sb.setMinimumSize(QtCore.QSize(50, 25))
                    self.name_sb.setMaximumSize(QtCore.QSize(50, 25))
                    self.name_sb.setStyleSheet(styles.styleSpinBox)
                    self.name_sb.setValue(0)
                    self.gridLayout_DIScreen.addWidget(self.name_sb, i, j, 1, 1)
                    
                j = j+1
                k = k+1
            j = 0
            i = i+1

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
        i = 0
        k = 0
        
        count = self.gridLayout_DIScreen.count() -1
        i = 0
        k = 0
    
        while(i < count):
            labelItem = self.gridLayout_DIScreen.itemAt(i).widget()
            labelItemValue = str(labelItem.objectName())
            #print("Label: " + str(labelItem))
            #print("Label Value: " + labelItemValue)
            self.gui.array_dataInput[0][k] = labelItemValue
            i = i+1
            
            spinboxItem = self.gridLayout_DIScreen.itemAt(i).widget()
            spinboxItemValue = str(spinboxItem.value())
            #print("SpinBox: " + str(spinboxItem))
            #print("SpinBox Value: " + spinboxItemValue)
            self.gui.array_dataInput[1][k] = spinboxItemValue
            i = i+1
            k = k+1

        #Testausgabe des gesamten Arrays
        #for j in range(len(self.gui.array_dataInput[0])):
        #    print(self.gui.array_dataInput[0][j], end=' ')
        #    print(self.gui.array_dataInput[1][j], end=' ')
        #    print()

    def reset_gridContent(self):
        i = 0
        k = 0
        
        count = self.gridLayout_DIScreen.count() -1
        i = 0
        k = 0
    
        while(i < count):
            labelItem = self.gridLayout_DIScreen.itemAt(i).widget()
            labelItemValue = str(labelItem.objectName())
            print("Label: " + str(labelItem))
            print("Label Value: " + labelItemValue)
            #self.gui.array_dataInput[0][k] = labelItemValue
            i = i+1
            
            spinboxItem = self.gridLayout_DIScreen.itemAt(i).widget()
            #print("SpinBox: " + str(spinboxItem))
            #spinboxItemValue = str(spinboxItem.value())
            #print("SpinBox Value Before: " + spinboxItemValue)
            spinboxItem.setValue(0)
            #spinboxItemValue = str(spinboxItem.value())
            #print("SpinBox Value After: " + spinboxItemValue)
            
            #Wenn Array auch zurückgesetzt werden soll, diese Zeile hier rein
            #self.gui.array_dataInput[1][k] = spinboxItemValue
            i = i+1
            k = k+1
        

# Analyze Preview Screen
class ui_analyzePvScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_analyzePvScreen, self).__init__()

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
        self.lyth_headline_AnalyzePreview.setSpacing(6)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_AnalyzePreview.sizePolicy().hasHeightForWidth())
        self.btn_info_AnalyzePreview.setSizePolicy(sizePolicy)
        self.btn_info_AnalyzePreview.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_AnalyzePreview.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_AnalyzePreview.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_AnalyzePreview.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_AnalyzePreview.setIcon(icon)
        self.btn_info_AnalyzePreview.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_AnalyzePreview.setObjectName("btn_info_AnalyzePreview")
        self.btn_info_AnalyzePreview.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_back_AnalyzePreview = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_back_AnalyzePreview.sizePolicy().hasHeightForWidth())
        self.btn_back_AnalyzePreview.setSizePolicy(sizePolicy)
        self.btn_back_AnalyzePreview.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_back_AnalyzePreview.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_back_AnalyzePreview.setStyleSheet(styles.styleSmallButton)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/back_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_AnalyzePreview.setIcon(icon2)
        self.btn_back_AnalyzePreview.setIconSize(QtCore.QSize(20, 20))
        self.btn_back_AnalyzePreview.setCheckable(True)
        self.btn_back_AnalyzePreview.setObjectName("btn_back_AnalyzePreview")
        self.btn_back_AnalyzePreview.clicked.connect(lambda: self.gui.change_screen_back())

        self.btn_startAnalyze = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_startAnalyze.sizePolicy().hasHeightForWidth())
        self.btn_startAnalyze.setSizePolicy(sizePolicy)
        self.btn_startAnalyze.setMinimumSize(QtCore.QSize(220, 40))
        self.btn_startAnalyze.setMaximumSize(QtCore.QSize(220, 40))
        self.btn_startAnalyze.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_startAnalyze.setText("Analyse starten")
        self.btn_startAnalyze.setCheckable(False)
        self.btn_startAnalyze.setFlat(False)
        self.btn_startAnalyze.setObjectName("btn_startAnalyze")

    def create_label(self):
        self.lbl_headline_AnalyzePreview = QtWidgets.QLabel(self)
        self.lbl_headline_AnalyzePreview.setStyleSheet(styles.styleHeadlines)
        self.lbl_headline_AnalyzePreview.setText("Datei Analyse")
        self.lbl_headline_AnalyzePreview.setObjectName("lbl_headline_AnalyzePreview")

        self.label_AnalyzePreview = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_AnalyzePreview.sizePolicy().hasHeightForWidth())
        self.label_AnalyzePreview.setSizePolicy(sizePolicy)
        self.label_AnalyzePreview.setStyleSheet(styles.styleText1)
        self.label_AnalyzePreview.setText("Vorschau")
        self.label_AnalyzePreview.setObjectName("label_AnalyzePreview")

    def create_preview(self):
        self.graphicsAnalyzePreview = QtWidgets.QGraphicsView(self)
        self.graphicsAnalyzePreview.setMinimumSize(QtCore.QSize(800, 420))
        self.graphicsAnalyzePreview.setMaximumSize(QtCore.QSize(800, 420))
        self.graphicsAnalyzePreview.setObjectName("graphicsAnalyzePreview")
        self.graphicsAnalyzePreview

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
        self.lyth_centerBig_AnalyzePreview.addWidget(self.graphicsAnalyzePreview)
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
class ui_analyzeScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_analyzeScreen, self).__init__()

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
        self.lyth_headline_Analyze.setSpacing(6)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_Analyze.sizePolicy().hasHeightForWidth())
        self.btn_info_Analyze.setSizePolicy(sizePolicy)
        self.btn_info_Analyze.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_Analyze.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_Analyze.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_Analyze.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_Analyze.setIcon(icon)
        self.btn_info_Analyze.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_Analyze.setObjectName("btn_info_Analyze")
        self.btn_info_Analyze.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_cancelAnalyze = QtWidgets.QPushButton(self)
        self.btn_cancelAnalyze.setMinimumSize(QtCore.QSize(220, 40))
        self.btn_cancelAnalyze.setMaximumSize(QtCore.QSize(220, 40))
        self.btn_cancelAnalyze.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_cancelAnalyze.setText("Abbrechen")
        self.btn_cancelAnalyze.setObjectName("btn_cancelAnalyze")

        self.btn_showResult = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_showResult.sizePolicy().hasHeightForWidth())
        self.btn_showResult.setSizePolicy(sizePolicy)
        self.btn_showResult.setMinimumSize(QtCore.QSize(220, 40))
        self.btn_showResult.setMaximumSize(QtCore.QSize(220, 40))
        self.btn_showResult.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_showResult.setText("Zur Auswertung")
        self.btn_showResult.setCheckable(False)
        self.btn_showResult.setFlat(False)
        self.btn_showResult.setObjectName("btn_showResult")


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
        self.label_IconTop.setMinimumSize(QtCore.QSize(75, 75))
        self.label_IconTop.setMaximumSize(QtCore.QSize(75, 75))
        self.label_IconTop.setObjectName("label_IconTop")

        self.label_IconMid = QtWidgets.QLabel(self)
        self.label_IconMid.setMinimumSize(QtCore.QSize(75, 75))
        self.label_IconMid.setMaximumSize(QtCore.QSize(75, 75))
        self.label_IconMid.setObjectName("label_IconMid")

        self.label_IconBottom = QtWidgets.QLabel(self)
        self.label_IconBottom.setMinimumSize(QtCore.QSize(75, 75))
        self.label_IconBottom.setMaximumSize(QtCore.QSize(75, 75))
        self.label_IconBottom.setObjectName("label_IconBottom")


    def create_preview(self):
        self.graphicsAnalyze = QtWidgets.QGraphicsView(self)
        self.graphicsAnalyze.setMinimumSize(QtCore.QSize(800, 420))
        self.graphicsAnalyze.setMaximumSize(QtCore.QSize(800, 420))
        self.graphicsAnalyze.setObjectName("graphicsAnalyze")

    
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
        self.lyth_centerBig_Analyze.addWidget(self.graphicsAnalyze)
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
      

# Result Screen
class ui_ResultScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_ResultScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("ResultScreen")

        self.create_layout()
        self.create_button()
        self.create_label()
        self.create_gridContent()
        self.create_spacer()
        self.add_items() 

    def create_layout(self):
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.lyth_headline_Result = QtWidgets.QHBoxLayout()
        self.lyth_headline_Result.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_Result.setSpacing(6)
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
        self.scrollArea_Result.setMinimumSize(QtCore.QSize(976, 0))
        self.scrollArea_Result.setMaximumSize(QtCore.QSize(1020, 16777215))
        self.scrollArea_Result.setSizeIncrement(QtCore.QSize(0, 0))
        self.scrollArea_Result.setWidgetResizable(True)
        self.scrollArea_Result.setObjectName("scrollArea_Result")

        self.scrollAreaResult = QtWidgets.QWidget()
        self.scrollAreaResult.setGeometry(QtCore.QRect(0, 0, 950, 360))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaResult.sizePolicy().hasHeightForWidth())
        self.scrollAreaResult.setSizePolicy(sizePolicy)
        self.scrollAreaResult.setMinimumSize(QtCore.QSize(950, 0))
        self.scrollAreaResult.setMaximumSize(QtCore.QSize(950, 16777215))
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_Result.sizePolicy().hasHeightForWidth())
        self.btn_info_Result.setSizePolicy(sizePolicy)
        self.btn_info_Result.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_Result.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_Result.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_Result.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_Result.setIcon(icon)
        self.btn_info_Result.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_Result.setObjectName("btn_info_Result")
        self.btn_info_Result.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_endResult = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_endResult.sizePolicy().hasHeightForWidth())
        self.btn_endResult.setSizePolicy(sizePolicy)
        self.btn_endResult.setMinimumSize(QtCore.QSize(220, 40))
        self.btn_endResult.setMaximumSize(QtCore.QSize(220, 40))
        self.btn_endResult.setStyleSheet(styles.styleBluebuttonsmall)
        self.btn_endResult.setText("Beenden")


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
        self.lbl_result.setMinimumSize(QtCore.QSize(80, 80))
        self.lbl_result.setMaximumSize(QtCore.QSize(80, 80))
        self.lbl_result.setStyleSheet("QLabel{\n""    font: bold 18pt \"MS Shell Dlg 2\" ;\n""    background-color: #00AA00;\n""    border-radius: 40px;\n""    color:white\n""}")
        self.lbl_result.setText("99%")
        self.lbl_result.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_result.setObjectName("lbl_result")

    def create_gridContent(self):

        self.lbl_input_result_1 = QtWidgets.QLabel(self.scrollAreaResult)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_input_result_1.sizePolicy().hasHeightForWidth())
        self.lbl_input_result_1.setSizePolicy(sizePolicy)
        self.lbl_input_result_1.setMinimumSize(QtCore.QSize(80, 30))
        self.lbl_input_result_1.setMaximumSize(QtCore.QSize(40, 30))
        self.lbl_input_result_1.setStyleSheet(styles.styleGridHeadline)
        self.lbl_input_result_1.setText("Eingabe")
        self.lbl_input_result_1.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_input_result_1.setObjectName("lbl_input_result_1")

        self.lbl_input_result_2 = QtWidgets.QLabel(self.scrollAreaResult)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_input_result_2.sizePolicy().hasHeightForWidth())
        self.lbl_input_result_2.setSizePolicy(sizePolicy)
        self.lbl_input_result_2.setMinimumSize(QtCore.QSize(80, 30))
        self.lbl_input_result_2.setMaximumSize(QtCore.QSize(40, 30))

        self.lbl_input_result_2.setStyleSheet(styles.styleGridHeadline)
        self.lbl_input_result_2.setText("Eingabe")
        self.lbl_input_result_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_input_result_2.setObjectName("lbl_input_result_2")

        self.lbl_input_result_3 = QtWidgets.QLabel(self.scrollAreaResult)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_input_result_3.sizePolicy().hasHeightForWidth())
        self.lbl_input_result_3.setSizePolicy(sizePolicy)
        self.lbl_input_result_3.setMinimumSize(QtCore.QSize(80, 30))
        self.lbl_input_result_3.setMaximumSize(QtCore.QSize(40, 30))

        self.lbl_input_result_3.setStyleSheet(styles.styleGridHeadline)
        self.lbl_input_result_3.setText("Eingabe")
        self.lbl_input_result_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_input_result_3.setObjectName("lbl_input_result_3")

        self.lbl_recogn_1 = QtWidgets.QLabel(self.scrollAreaResult)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_recogn_1.sizePolicy().hasHeightForWidth())
        self.lbl_recogn_1.setSizePolicy(sizePolicy)
        self.lbl_recogn_1.setMinimumSize(QtCore.QSize(80, 30))
        self.lbl_recogn_1.setMaximumSize(QtCore.QSize(40, 30))
        self.lbl_recogn_1.setStyleSheet(styles.styleGridHeadline)
        self.lbl_recogn_1.setText("Erkannt")
        self.lbl_recogn_1.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_recogn_1.setObjectName("lbl_recogn_1")
        

        self.lbl_recogn_2 = QtWidgets.QLabel(self.scrollAreaResult)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_recogn_2.sizePolicy().hasHeightForWidth())
        self.lbl_recogn_2.setSizePolicy(sizePolicy)
        self.lbl_recogn_2.setMinimumSize(QtCore.QSize(80, 30))
        self.lbl_recogn_2.setMaximumSize(QtCore.QSize(40, 30))
        self.lbl_recogn_2.setStyleSheet(styles.styleGridHeadline)
        self.lbl_recogn_2.setText("Erkannt")
        self.lbl_recogn_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_recogn_2.setObjectName("lbl_recogn_2")
        
        self.lbl_recogn_3 = QtWidgets.QLabel(self.scrollAreaResult)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_recogn_3.sizePolicy().hasHeightForWidth())
        self.lbl_recogn_3.setSizePolicy(sizePolicy)
        self.lbl_recogn_3.setMinimumSize(QtCore.QSize(80, 30))
        self.lbl_recogn_3.setMaximumSize(QtCore.QSize(40, 30))
        self.lbl_recogn_3.setStyleSheet(styles.styleGridHeadline)
        self.lbl_recogn_3.setText("Erkannt")
        self.lbl_recogn_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_recogn_3.setObjectName("lbl_recogn_3")
             
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
        self.gridLayout_Result.addWidget(self.lbl_input_result_1, 0, 1, 1, 1)
        self.gridLayout_Result.addWidget(self.lbl_input_result_2, 0, 4, 1, 1)
        self.gridLayout_Result.addWidget(self.lbl_input_result_3, 0, 7, 1, 1)
        self.gridLayout_Result.addWidget(self.lbl_recogn_1, 0, 2, 1, 1)
        self.gridLayout_Result.addWidget(self.lbl_recogn_2, 0, 5, 1, 1)
        self.gridLayout_Result.addWidget(self.lbl_recogn_3, 0, 8, 1, 1)
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

       
# Demo Data Screen
class ui_DemoDataScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_DemoDataScreen, self).__init__()

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
        self.lyth_headline_DemoData.setSpacing(6)
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
        self.scrollArea_DemoData.setMinimumSize(QtCore.QSize(976, 0))
        self.scrollArea_DemoData.setMaximumSize(QtCore.QSize(1020, 16777215))
        self.scrollArea_DemoData.setSizeIncrement(QtCore.QSize(0, 0))
        self.scrollArea_DemoData.setWidgetResizable(True)
        self.scrollArea_DemoData.setObjectName("scrollArea_DemoData")
        self.scrollAreaWidget_DemoData = QtWidgets.QWidget()
        self.scrollAreaWidget_DemoData.setGeometry(QtCore.QRect(0, 0, 950, 597))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidget_DemoData.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidget_DemoData.setSizePolicy(sizePolicy)
        self.scrollAreaWidget_DemoData.setMinimumSize(QtCore.QSize(950, 0))
        self.scrollAreaWidget_DemoData.setMaximumSize(QtCore.QSize(950, 16777215))
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
        self.lyth_bottom_DemoData.setSpacing(6)
        self.lyth_bottom_DemoData.setObjectName("lyth_bottom_DemoData")


    def create_button(self):
        self.btn_info_DemoData = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_DemoData.sizePolicy().hasHeightForWidth())
        self.btn_info_DemoData.setSizePolicy(sizePolicy)
        self.btn_info_DemoData.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_DemoData.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_DemoData.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_DemoData.setStyleSheet(styles.styleSmallButton)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_DemoData.setIcon(icon)
        self.btn_info_DemoData.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_DemoData.setObjectName("btn_info_DemoData")
        self.btn_info_DemoData.clicked.connect(lambda: self.gui.infoscreen.show())

        self.btn_ok_demoData = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_ok_demoData.sizePolicy().hasHeightForWidth())
        self.btn_ok_demoData.setSizePolicy(sizePolicy)
        self.btn_ok_demoData.setMinimumSize(QtCore.QSize(220, 40))
        self.btn_ok_demoData.setMaximumSize(QtCore.QSize(220, 40))
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_DIScreen_DemoData.sizePolicy().hasHeightForWidth())
        self.label_DIScreen_DemoData.setSizePolicy(sizePolicy)
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

        i = 0
        j = 0
        
        with open(filepath, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            
            next(csv_reader)

            for line in csv_reader:
                if(int(line[2]) > 0):

                    self.sign_id = ":/signs/" + line[0]
                    self.sign_count = line[2]

                    self.name_sign = QtWidgets.QLabel(self.scrollAreaWidget_DemoData)
                    self.name_sign.setMinimumSize(QtCore.QSize(48, 48))
                    self.name_sign.setMaximumSize(QtCore.QSize(48, 48))
                    self.name_sign.setPixmap(QtGui.QPixmap(self.sign_id))
                    self.name_sign.setScaledContents(True)
                    self.gridLayout_DemoData.addWidget(self.name_sign, i,j,1,1)

                    j = j+1

                    self.lbl_amount = QtWidgets.QLabel(self.scrollAreaWidget_DemoData)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.lbl_amount.sizePolicy().hasHeightForWidth())
                    self.lbl_amount.setSizePolicy(sizePolicy)
                    self.lbl_amount.setMinimumSize(QtCore.QSize(40, 30))
                    self.lbl_amount.setMaximumSize(QtCore.QSize(40, 30))
                    self.lbl_amount.setObjectName("lbl_amount")
                    self.lbl_amount.setStyleSheet(styles.styleText1)
                    self.lbl_amount.setText(self.sign_count)
                    self.gridLayout_DemoData.addWidget(self.lbl_amount, i, j, 1, 1)

                    j = j+1
                    if(j > 7):
                        j = 0
                        i = i+1

    def delete_grid(self):
        

        if(self.gridLayout_DemoData.itemAt(0) is None):
            print("empty")
        else:
            #print("not empty")
            
            count=self.gridLayout_DemoData.count()
            i = count
            while(i >= 0):
                print("removing item " + str(i))
                #self.gridLayout_DemoData.itemAt(i).widget.setParent(None)
                self.gridLayout_DemoData.removeItem(self.gridLayout_DemoData.itemAt(i))
                i=i-1       


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
class ui_InfoScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_InfoScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("InfoScreen")
        self.setFixedSize(800,700)
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
        self.lyth_headline_Info.setSpacing(6)
        self.lyth_headline_Info.setObjectName("lyth_headline_Info")
        self.lbl_headline_Info = QtWidgets.QLabel(self)

        self.verticalLayout_12.addLayout(self.lyth_headline_Info)
        self.lytv_centerInfo = QtWidgets.QVBoxLayout()
        self.lytv_centerInfo.setContentsMargins(60, 45, -1, -1)
        self.lytv_centerInfo.setSpacing(20)
        self.lytv_centerInfo.setObjectName("lytv_centerInfo")

        self.lyth_bottom_Info = QtWidgets.QHBoxLayout()
        self.lyth_bottom_Info.setContentsMargins(-1, -1, 2, -1)
        self.lyth_bottom_Info.setObjectName("lyth_bottom_Info")

    def create_button(self):
        self.btn_closeInfo = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_closeInfo.sizePolicy().hasHeightForWidth())
        self.btn_closeInfo.setSizePolicy(sizePolicy)
        self.btn_closeInfo.setMinimumSize(QtCore.QSize(220, 40))
        self.btn_closeInfo.setMaximumSize(QtCore.QSize(220, 40))
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
        self.label_Logo.setMaximumSize(QtCore.QSize(500, 16777215))
        self.label_Logo.setPixmap(QtGui.QPixmap(":/icons/logoSK_big_1"))
        self.label_Logo.setObjectName("label_Logo")

        self.label_infoText = QtWidgets.QLabel(self)
        self.label_infoText.setStyleSheet(styles.styleText1)      
        self.label_infoText.setText("Schilder Kröten GmbH\n""Musterstraße 1\n""12345 Musterstadt\n""\n""Ansprechpartner:\n""Herr Mayer\n""\n""0123-456789\n""")
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
