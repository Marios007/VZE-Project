from PyQt5 import QtCore, QtGui, QtWidgets
import gui.styles as styles
import gui.image_ressources as image_ressources


class VzeGui(QtWidgets.QMainWindow):

    def __init__(self, logicInterface):
        QtWidgets.QMainWindow.__init__(self)
        print ("loading UI")
       
        self.logic = logicInterface
        # Setting Window Title and Icon
        self.setWindowTitle("VerkehrsZeichenErkennung VZE")
        #self.setWindowIcon(QtGui.QIcon("gui/pics/Logo_Schild_v1_2020-08-10_TB.png"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/logo_schild"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
    


       # Size of window is always half size of availabe window
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
        
        #Build UI with each screen
        print ("Build screens")
        self.startscreen = ui_startscreen(self.logic, self)
        self.stackedWidget.addWidget(self.startscreen)

        self.demoscreen = ui_demoscreen(self.logic, self)
        self.stackedWidget.addWidget(self.demoscreen)

        self.previewscreen = ui_previewscreen(self.logic, self)
        self.stackedWidget.addWidget(self.previewscreen)

        self.analyzepvscreen = ui_analyzePvScreen(self.logic, self)
        self.stackedWidget.addWidget(self.analyzepvscreen)



        self.verticalLayout.addWidget(self.stackedWidget)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(window)

       

# Start Screen
class ui_startscreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_startscreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

    #def create_layout(self):
    
    #def create_button(self):

    
    #def create_label(self):
    
    
    #def add_items(self):

        self.setObjectName("StartScreen")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
    
        self.lyth_headline = QtWidgets.QHBoxLayout()
        self.lyth_headline.setContentsMargins(20, -1, 20, 0)
        self.lyth_headline.setObjectName("lyth_headline")
        
        self.lbl_willkommen = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_willkommen.setFont(font)
        self.lbl_willkommen.setStyleSheet("color: rgb(242, 141, 27);")
        self.lbl_willkommen.setObjectName("lbl_willkommen")
        self.lyth_headline.addWidget(self.lbl_willkommen)
        
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_headline.addItem(spacerItem)
        
        # Button Info Startscreen
        self.btn_info_startscreen = QtWidgets.QPushButton(self)
        self.btn_info_startscreen.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_startscreen.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_startscreen.setStatusTip("")
        self.btn_info_startscreen.setWhatsThis("")
        self.btn_info_startscreen.setAccessibleName("")
        self.btn_info_startscreen.setAccessibleDescription("")
        self.btn_info_startscreen.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")
        self.btn_info_startscreen.setText("")
        icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("gui/pics/info_logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_startscreen.setIcon(icon)
        self.btn_info_startscreen.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_startscreen.setCheckable(False)
        self.btn_info_startscreen.setChecked(False)
        self.btn_info_startscreen.setObjectName("btn_info_startscreen")
        self.lyth_headline.addWidget(self.btn_info_startscreen)

        self.verticalLayout_2.addLayout(self.lyth_headline)
        
        self.lytv_bigCenter = QtWidgets.QVBoxLayout()
        self.lytv_bigCenter.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytv_bigCenter.setContentsMargins(0, -1, 0, -1)
        self.lytv_bigCenter.setObjectName("lytv_bigCenter")
        self.lyth_smallText = QtWidgets.QHBoxLayout()
        self.lyth_smallText.setContentsMargins(-1, 0, -1, -1)
        self.lyth_smallText.setObjectName("lyth_smallText")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_smallText.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lyth_smallText.addItem(spacerItem2)
        self.lytv_bigCenter.addLayout(self.lyth_smallText)
        self.lyth_bigBtn = QtWidgets.QHBoxLayout()
        self.lyth_bigBtn.setObjectName("lyth_bigBtn")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bigBtn.addItem(spacerItem3)
        self.btn_loadFile = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_loadFile.sizePolicy().hasHeightForWidth())
        self.btn_loadFile.setSizePolicy(sizePolicy)
        self.btn_loadFile.setMinimumSize(QtCore.QSize(350, 220))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.btn_loadFile.setFont(font)
        self.btn_loadFile.setStyleSheet(styles.styleBluebutton)
        self.btn_loadFile.setCheckable(False)
        self.btn_loadFile.setFlat(False)
        self.btn_loadFile.setObjectName("btn_loadFile")
        self.lyth_bigBtn.addWidget(self.btn_loadFile)
        spacerItem4 = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lyth_bigBtn.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bigBtn.addItem(spacerItem5)
        self.btn_demoToDemo = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_demoToDemo.sizePolicy().hasHeightForWidth())
        
        self.btn_demoToDemo.setSizePolicy(sizePolicy)
        self.btn_demoToDemo.setMinimumSize(QtCore.QSize(350, 220))
        self.btn_demoToDemo.setStyleSheet(styles.styleBluebutton)
        self.btn_demoToDemo.setObjectName("btn_demoToDemo")
        self.lyth_bigBtn.addWidget(self.btn_demoToDemo)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bigBtn.addItem(spacerItem6)
        self.lytv_bigCenter.addLayout(self.lyth_bigBtn)
        self.lyth_smallBtn = QtWidgets.QHBoxLayout()
        self.lyth_smallBtn.setObjectName("lyth_smallBtn")
        spacerItem7 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lyth_smallBtn.addItem(spacerItem7)
        self.lytv_bigCenter.addLayout(self.lyth_smallBtn)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lytv_bigCenter.addItem(spacerItem8)
        self.verticalLayout_2.addLayout(self.lytv_bigCenter)
        self.lyth_bottom = QtWidgets.QHBoxLayout()
        self.lyth_bottom.setObjectName("lyth_bottom")
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lyth_bottom.addItem(spacerItem9)
        self.verticalLayout_2.addLayout(self.lyth_bottom)
        

        self.lbl_willkommen.setText(("Willkommen"))
        #self.btn_info_startscreen.setText((""))
        self.btn_loadFile.setText(("Datei auswählen"))
        self.btn_demoToDemo.setText(("Demo auswählen"))

        
        self.btn_loadFile.setToolTip('Laden eines Videos oder Bildes')
        self.btn_loadFile.released.connect(self.logic.loadFile)
        self.btn_loadFile.clicked.connect(lambda: self.gui.stackedWidget.setCurrentIndex(2))

        self.btn_demoToDemo.setToolTip('Demo Videos wählen')
        self.btn_demoToDemo.clicked.connect(lambda: self.logic.doSomething())
        self.btn_demoToDemo.clicked.connect(lambda: self.gui.stackedWidget.setCurrentIndex(1))

# Demo Screen
class ui_demoscreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_demoscreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("DemoScreen")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lyth_headline_demoscreen = QtWidgets.QHBoxLayout()
        self.lyth_headline_demoscreen.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_demoscreen.setSpacing(6)
        self.lyth_headline_demoscreen.setObjectName("lyth_headline_demoscreen")
        self.lbl_demo = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_demo.setFont(font)
        self.lbl_demo.setStyleSheet("color: rgb(242, 141, 27);")
        self.lbl_demo.setObjectName("lbl_demo")
        self.lyth_headline_demoscreen.addWidget(self.lbl_demo)
        spacerItem10 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_headline_demoscreen.addItem(spacerItem10)
        
        # Button Info Demoscreen
        self.btn_info_demoscreen = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_demoscreen.sizePolicy().hasHeightForWidth())
        self.btn_info_demoscreen.setSizePolicy(sizePolicy)
        self.btn_info_demoscreen.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_demoscreen.setMaximumSize(QtCore.QSize(140, 45))
        #self.btn_info_demoscreen.setStatusTip("")
        #self.btn_info_demoscreen.setWhatsThis("")
        #self.btn_info_demoscreen.setAccessibleName("")
        #self.btn_info_demoscreen.setAccessibleDescription("")
        self.btn_info_demoscreen.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")
        self.btn_info_demoscreen.setText("")
        icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("gui/pics/info_logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_demoscreen.setIcon(icon)
        self.btn_info_demoscreen.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_demoscreen.setObjectName("btn_info_demoscreen")
        self.lyth_headline_demoscreen.addWidget(self.btn_info_demoscreen)
        self.verticalLayout_3.addLayout(self.lyth_headline_demoscreen)
        
        
        # Layout big center
        self.lytv_bigCenter_demoScreen = QtWidgets.QVBoxLayout()
        self.lytv_bigCenter_demoScreen.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytv_bigCenter_demoScreen.setContentsMargins(0, -1, 0, -1)
        self.lytv_bigCenter_demoScreen.setObjectName("lytv_bigCenter_demoScreen")
        
        self.lyth_smallText_Demo = QtWidgets.QHBoxLayout()
        self.lyth_smallText_Demo.setContentsMargins(20, 0, -1, -1)
        self.lyth_smallText_Demo.setObjectName("lyth_smallText_Demo")

        # Label Text and spacer
        self.label_demotext = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_demotext.sizePolicy().hasHeightForWidth())
        self.label_demotext.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_demotext.setFont(font)
        #self.label_demotext.setStatusTip("")
        #self.label_demotext.setWhatsThis("")
        #self.label_demotext.setAccessibleName("")
        #self.label_demotext.setAccessibleDescription("")
        self.label_demotext.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_demotext.setObjectName("label_demotext")
        self.lyth_smallText_Demo.addWidget(self.label_demotext, 0, QtCore.Qt.AlignTop)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_smallText_Demo.addItem(spacerItem11)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lyth_smallText_Demo.addItem(spacerItem12)
        self.lytv_bigCenter_demoScreen.addLayout(self.lyth_smallText_Demo)

        # Layout big in big center layout with the 2 buttons
        self.lyth_bigBtn_Demo = QtWidgets.QHBoxLayout()
        self.lyth_bigBtn_Demo.setObjectName("lyth_bigBtn_Demo")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bigBtn_Demo.addItem(spacerItem13)
        self.btn_demoSonne = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_demoSonne.sizePolicy().hasHeightForWidth())
        self.btn_demoSonne.setSizePolicy(sizePolicy)
        self.btn_demoSonne.setMinimumSize(QtCore.QSize(350, 220))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.btn_demoSonne.setFont(font)
        self.btn_demoSonne.setStyleSheet("QPushButton{\n""    font: 75 26pt \"MS Shell Dlg 2\" ;\n""    background-color: #1C4481;\n""    border-radius: 5px;\n""    color:white\n""}\n""\n""QPushButton:hover{\n""    border: 2px solid rgb(255, 255, 255)\n""}")
        self.btn_demoSonne.setCheckable(False)
        self.btn_demoSonne.setFlat(False)
        self.btn_demoSonne.setObjectName("btn_demoSonne")
        self.lyth_bigBtn_Demo.addWidget(self.btn_demoSonne)
        spacerItem14 = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lyth_bigBtn_Demo.addItem(spacerItem14)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bigBtn_Demo.addItem(spacerItem15)
        self.btn_demoRegen = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_demoRegen.sizePolicy().hasHeightForWidth())
        self.btn_demoRegen.setSizePolicy(sizePolicy)
        self.btn_demoRegen.setMinimumSize(QtCore.QSize(350, 220))
        self.btn_demoRegen.setStyleSheet("QPushButton{\n""    font: 75 26pt \"MS Shell Dlg 2\" ;\n""    background-color: #1C4481;\n""    border-radius:5px;\n""    color:white\n""}\n""\n""QPushButton:hover{\n""    border: 2px solid rgb(255, 255, 255)\n""}")
        self.btn_demoRegen.setIconSize(QtCore.QSize(51, 0))
        self.btn_demoRegen.setObjectName("btn_demoRegen")
        self.lyth_bigBtn_Demo.addWidget(self.btn_demoRegen)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bigBtn_Demo.addItem(spacerItem16)
        self.lytv_bigCenter_demoScreen.addLayout(self.lyth_bigBtn_Demo)
        self.lyth_smallBtn_demoscreen = QtWidgets.QHBoxLayout()
        self.lyth_smallBtn_demoscreen.setObjectName("lyth_smallBtn_demoscreen")
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_smallBtn_demoscreen.addItem(spacerItem17)
        
        icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap("gui/pics/data-icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icons/data_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.btn_dataSonne = QtWidgets.QPushButton(self)
        self.btn_dataSonne.setMinimumSize(QtCore.QSize(55, 55))
        self.btn_dataSonne.setMaximumSize(QtCore.QSize(55, 55))
        self.btn_dataSonne.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")

        self.btn_dataSonne.setIcon(icon1)
        self.btn_dataSonne.setIconSize(QtCore.QSize(55, 55))
        self.btn_dataSonne.setObjectName("btn_dataSonne")
        self.lyth_smallBtn_demoscreen.addWidget(self.btn_dataSonne)

        spacerItem18 = QtWidgets.QSpacerItem(370, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.lyth_smallBtn_demoscreen.addItem(spacerItem18)
        
        self.btn_dataRegen = QtWidgets.QPushButton(self)
        self.btn_dataRegen.setMinimumSize(QtCore.QSize(55, 55))
        self.btn_dataRegen.setMaximumSize(QtCore.QSize(55, 55))
        self.btn_dataRegen.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")
        self.btn_dataRegen.setIcon(icon1)
        self.btn_dataRegen.setIconSize(QtCore.QSize(55, 55))
        self.btn_dataRegen.setObjectName("btn_dataRegen")
        self.lyth_smallBtn_demoscreen.addWidget(self.btn_dataRegen)
        
        
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_smallBtn_demoscreen.addItem(spacerItem19)
        spacerItem20 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lyth_smallBtn_demoscreen.addItem(spacerItem20)
        self.lytv_bigCenter_demoScreen.addLayout(self.lyth_smallBtn_demoscreen)
        spacerItem21 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lytv_bigCenter_demoScreen.addItem(spacerItem21)
        self.verticalLayout_3.addLayout(self.lytv_bigCenter_demoScreen)
        self.lyth_bottom_demoscreen = QtWidgets.QHBoxLayout()
        self.lyth_bottom_demoscreen.setObjectName("lyth_bottom_demoscreen")
        
        # Button Back in Demoscreen
        self.btn_back_demoscreen = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_back_demoscreen.sizePolicy().hasHeightForWidth())
        self.btn_back_demoscreen.setSizePolicy(sizePolicy)
        self.btn_back_demoscreen.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_back_demoscreen.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_back_demoscreen.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")
        self.btn_back_demoscreen.setText("")
        icon2 = QtGui.QIcon()
        #icon2.addPixmap(QtGui.QPixmap("gui/pics/back_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/icons/back_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_demoscreen.setIcon(icon2)
        self.btn_back_demoscreen.setIconSize(QtCore.QSize(20, 20))
        self.btn_back_demoscreen.setObjectName("btn_back_demoscreen")
        self.lyth_bottom_demoscreen.addWidget(self.btn_back_demoscreen)


        spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bottom_demoscreen.addItem(spacerItem22)
        spacerItem23 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lyth_bottom_demoscreen.addItem(spacerItem23)
        self.verticalLayout_3.addLayout(self.lyth_bottom_demoscreen)

    
        
        # Set texts

        self.lbl_demo.setText(("Demo"))
        #self.btn_info_demoscreen.setText((""))
        self.label_demotext.setText(("Wählen Sie ein Demovideo aus"))
        self.btn_demoSonne.setText(("Video mit Sonne"))
        self.btn_demoRegen.setText(("Video mit Regen"))
        #self.btn_dataSonne.setText((""))
        #self.btn_dataRegen.setText((""))
        #self.btn_back_demoscreen.setText((""))

        # Button handler with interface
        self.btn_back_demoscreen.clicked.connect(lambda: self.gui.stackedWidget.setCurrentIndex(0))
# Preview Screen
class ui_previewscreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_previewscreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

        self.setObjectName("PreviewScreen")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lyth_headline_previewScreen = QtWidgets.QHBoxLayout()
        self.lyth_headline_previewScreen.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_previewScreen.setSpacing(6)
        self.lyth_headline_previewScreen.setObjectName("lyth_headline_previewScreen")
        self.lbl_headline_preview = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_headline_preview.setFont(font)
        self.lbl_headline_preview.setStyleSheet("color: rgb(242, 141, 27);")
        self.lbl_headline_preview.setObjectName("lbl_headline_preview")
        self.lyth_headline_previewScreen.addWidget(self.lbl_headline_preview)
        spacerItem24 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_headline_previewScreen.addItem(spacerItem24)

        # Button Info preview screen
        self.btn_info_previewScreen = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_previewScreen.sizePolicy().hasHeightForWidth())
        self.btn_info_previewScreen.setSizePolicy(sizePolicy)
        self.btn_info_previewScreen.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_previewScreen.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_previewScreen.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_previewScreen.setStatusTip("")
        self.btn_info_previewScreen.setWhatsThis("")
        self.btn_info_previewScreen.setAccessibleName("")
        self.btn_info_previewScreen.setAccessibleDescription("")
        self.btn_info_previewScreen.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")
        icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("gui/pics/info_logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icons/info_logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_previewScreen.setIcon(icon)
        self.btn_info_previewScreen.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_previewScreen.setObjectName("btn_info_previewScreen")
        self.lyth_headline_previewScreen.addWidget(self.btn_info_previewScreen)
        self.verticalLayout_4.addLayout(self.lyth_headline_previewScreen)
        self.lytv_bigCenter_previewScreen = QtWidgets.QVBoxLayout()
        self.lytv_bigCenter_previewScreen.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytv_bigCenter_previewScreen.setContentsMargins(0, -1, 0, -1)
        self.lytv_bigCenter_previewScreen.setObjectName("lytv_bigCenter_previewScreen")
        self.lyth_smallText_previewScreen = QtWidgets.QHBoxLayout()
        self.lyth_smallText_previewScreen.setContentsMargins(20, 0, -1, -1)
        self.lyth_smallText_previewScreen.setObjectName("lyth_smallText_previewScreen")
        self.label_preview = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_preview.sizePolicy().hasHeightForWidth())
        self.label_preview.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_preview.setFont(font)
        self.label_preview.setStatusTip("")
        self.label_preview.setWhatsThis("")
        self.label_preview.setAccessibleName("")
        self.label_preview.setAccessibleDescription("")
        self.label_preview.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_preview.setObjectName("label_preview")
        self.lyth_smallText_previewScreen.addWidget(self.label_preview, 0, QtCore.Qt.AlignTop)
        spacerItem25 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_smallText_previewScreen.addItem(spacerItem25)
        spacerItem26 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lyth_smallText_previewScreen.addItem(spacerItem26)
        self.lytv_bigCenter_previewScreen.addLayout(self.lyth_smallText_previewScreen)
        self.lyth_centerBig = QtWidgets.QHBoxLayout()
        self.lyth_centerBig.setObjectName("lyth_centerBig")
        spacerItem27 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_centerBig.addItem(spacerItem27)

        # graphics view to add a picture
        self.graphicsPreview = QtWidgets.QGraphicsView(self)
        self.graphicsPreview.setMinimumSize(QtCore.QSize(800, 420))
        self.graphicsPreview.setMaximumSize(QtCore.QSize(800, 420))
        self.graphicsPreview.setObjectName("graphicsPreview")
        self.lyth_centerBig.addWidget(self.graphicsPreview)
        spacerItem28 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_centerBig.addItem(spacerItem28)
        spacerItem29 = QtWidgets.QSpacerItem(0, 450, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lyth_centerBig.addItem(spacerItem29)
        self.lytv_bigCenter_previewScreen.addLayout(self.lyth_centerBig)
        self.lyth_blwCenter = QtWidgets.QHBoxLayout()
        self.lyth_blwCenter.setObjectName("lyth_blwCenter")
        self.lytv_bigCenter_previewScreen.addLayout(self.lyth_blwCenter)
        spacerItem30 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lytv_bigCenter_previewScreen.addItem(spacerItem30)
        self.label_loadSuccess = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_loadSuccess.setFont(font)
        self.label_loadSuccess.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_loadSuccess.setObjectName("label_loadSuccess")
        self.lytv_bigCenter_previewScreen.addWidget(self.label_loadSuccess, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_4.addLayout(self.lytv_bigCenter_previewScreen)
        self.lyth_bottom_previewScreen = QtWidgets.QHBoxLayout()
        self.lyth_bottom_previewScreen.setContentsMargins(-1, -1, 20, -1)
        self.lyth_bottom_previewScreen.setObjectName("lyth_bottom_previewScreen")
        

        # Button back
        self.btn_back_previewScreen = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_back_previewScreen.sizePolicy().hasHeightForWidth())
        self.btn_back_previewScreen.setSizePolicy(sizePolicy)
        self.btn_back_previewScreen.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_back_previewScreen.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(False)
        font.setWeight(50)
        self.btn_back_previewScreen.setFont(font)
        self.btn_back_previewScreen.setStatusTip("")
        self.btn_back_previewScreen.setWhatsThis("")
        self.btn_back_previewScreen.setAccessibleName("")
        self.btn_back_previewScreen.setAccessibleDescription("")
        self.btn_back_previewScreen.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")
        icon2 = QtGui.QIcon()
        #icon2.addPixmap(QtGui.QPixmap("gui/pics/back_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/icons/back_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_previewScreen.setIcon(icon2)
        self.btn_back_previewScreen.setIconSize(QtCore.QSize(20, 20))
        self.btn_back_previewScreen.setObjectName("btn_back_previewScreen")
        self.lyth_bottom_previewScreen.addWidget(self.btn_back_previewScreen)
        spacerItem31 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bottom_previewScreen.addItem(spacerItem31)
        spacerItem32 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lyth_bottom_previewScreen.addItem(spacerItem32)
        self.btn_next_preview = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_next_preview.sizePolicy().hasHeightForWidth())
        self.btn_next_preview.setSizePolicy(sizePolicy)
        self.btn_next_preview.setMinimumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.btn_next_preview.setFont(font)
        self.btn_next_preview.setStyleSheet(styles.styleBluebutton)
        self.btn_next_preview.setCheckable(False)
        self.btn_next_preview.setFlat(False)
        self.btn_next_preview.setObjectName("btn_next_preview")
        self.lyth_bottom_previewScreen.addWidget(self.btn_next_preview)
        self.verticalLayout_4.addLayout(self.lyth_bottom_previewScreen)
        

        self.lbl_headline_preview.setText("Datei Analyze")
        self.btn_info_previewScreen.setText("")
        self.label_preview.setText("Vorschau")
        self.label_loadSuccess.setText("Datei erfolgreich geladen. ")
        self.btn_back_previewScreen.setText("")
        self.btn_next_preview.setText("Weiter")

        self.btn_back_previewScreen.clicked.connect(lambda: self.gui.stackedWidget.setCurrentIndex(0))



# DI Screen
class ui_DIScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_DIScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui


# Analyze Preview Screen
class ui_analyzePvScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_analyzePvScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui


        self.setObjectName("AnalyzePreviewScreen")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lyth_headline_AnalyzePreview = QtWidgets.QHBoxLayout()
        self.lyth_headline_AnalyzePreview.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_AnalyzePreview.setSpacing(6)
        self.lyth_headline_AnalyzePreview.setObjectName("lyth_headline_AnalyzePreview")
        self.lbl_headline_AnalyzePreview = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_headline_AnalyzePreview.setFont(font)
        self.lbl_headline_AnalyzePreview.setStatusTip("")
        self.lbl_headline_AnalyzePreview.setWhatsThis("")
        self.lbl_headline_AnalyzePreview.setAccessibleName("")
        self.lbl_headline_AnalyzePreview.setAccessibleDescription("")
        self.lbl_headline_AnalyzePreview.setStyleSheet("color: rgb(242, 141, 27);")
        self.lbl_headline_AnalyzePreview.setObjectName("lbl_headline_AnalyzePreview")
        self.lyth_headline_AnalyzePreview.addWidget(self.lbl_headline_AnalyzePreview)
        spacerItem43 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_headline_AnalyzePreview.addItem(spacerItem43)
        self.btn_info_AnalyzePreview = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_AnalyzePreview.sizePolicy().hasHeightForWidth())
        self.btn_info_AnalyzePreview.setSizePolicy(sizePolicy)
        self.btn_info_AnalyzePreview.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_AnalyzePreview.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_AnalyzePreview.setBaseSize(QtCore.QSize(0, 0))
        self.btn_info_AnalyzePreview.setStatusTip("")
        self.btn_info_AnalyzePreview.setWhatsThis("")
        self.btn_info_AnalyzePreview.setAccessibleName("")
        self.btn_info_AnalyzePreview.setAccessibleDescription("")
        self.btn_info_AnalyzePreview.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")
        self.btn_info_AnalyzePreview.setText("")
        self.btn_info_AnalyzePreview.setIcon(':/icons/logo_schild')
        self.btn_info_AnalyzePreview.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_AnalyzePreview.setObjectName("btn_info_AnalyzePreview")
        self.lyth_headline_AnalyzePreview.addWidget(self.btn_info_AnalyzePreview)
        self.verticalLayout_5.addLayout(self.lyth_headline_AnalyzePreview)
        self.lytv_bigCenter_AnalyzePreview = QtWidgets.QVBoxLayout()
        self.lytv_bigCenter_AnalyzePreview.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytv_bigCenter_AnalyzePreview.setContentsMargins(0, -1, 0, -1)
        self.lytv_bigCenter_AnalyzePreview.setObjectName("lytv_bigCenter_AnalyzePreview")
        self.lyth_smallText_AnalyzePreview = QtWidgets.QHBoxLayout()
        self.lyth_smallText_AnalyzePreview.setContentsMargins(20, 0, -1, -1)
        self.lyth_smallText_AnalyzePreview.setObjectName("lyth_smallText_AnalyzePreview")
        self.label_AnalyzePreview = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_AnalyzePreview.sizePolicy().hasHeightForWidth())
        self.label_AnalyzePreview.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label_AnalyzePreview.setFont(font)
        self.label_AnalyzePreview.setStatusTip("")
        self.label_AnalyzePreview.setWhatsThis("")
        self.label_AnalyzePreview.setAccessibleName("")
        self.label_AnalyzePreview.setAccessibleDescription("")
        self.label_AnalyzePreview.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_AnalyzePreview.setObjectName("label_AnalyzePreview")
        self.lyth_smallText_AnalyzePreview.addWidget(self.label_AnalyzePreview, 0, QtCore.Qt.AlignTop)
        spacerItem44 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_smallText_AnalyzePreview.addItem(spacerItem44)
        spacerItem45 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lyth_smallText_AnalyzePreview.addItem(spacerItem45)
        self.lytv_bigCenter_AnalyzePreview.addLayout(self.lyth_smallText_AnalyzePreview)
        self.lyth_centerBig_AnalyzePreview = QtWidgets.QHBoxLayout()
        self.lyth_centerBig_AnalyzePreview.setObjectName("lyth_centerBig_AnalyzePreview")
        spacerItem46 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_centerBig_AnalyzePreview.addItem(spacerItem46)
        self.graphicsAnalyzePreview = QtWidgets.QGraphicsView(self)
        self.graphicsAnalyzePreview.setMinimumSize(QtCore.QSize(800, 420))
        self.graphicsAnalyzePreview.setMaximumSize(QtCore.QSize(800, 420))
        self.graphicsAnalyzePreview.setObjectName("graphicsAnalyzePreview")
        self.lyth_centerBig_AnalyzePreview.addWidget(self.graphicsAnalyzePreview)
        spacerItem47 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_centerBig_AnalyzePreview.addItem(spacerItem47)
        spacerItem48 = QtWidgets.QSpacerItem(0, 450, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lyth_centerBig_AnalyzePreview.addItem(spacerItem48)
        self.lytv_bigCenter_AnalyzePreview.addLayout(self.lyth_centerBig_AnalyzePreview)
        self.lyth_blwCenter_AnalyzePreview = QtWidgets.QHBoxLayout()
        self.lyth_blwCenter_AnalyzePreview.setObjectName("lyth_blwCenter_AnalyzePreview")
        self.lytv_bigCenter_AnalyzePreview.addLayout(self.lyth_blwCenter_AnalyzePreview)
        spacerItem49 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lytv_bigCenter_AnalyzePreview.addItem(spacerItem49)
        self.verticalLayout_5.addLayout(self.lytv_bigCenter_AnalyzePreview)
        self.lyth_bottom_AnalyzePreview = QtWidgets.QHBoxLayout()
        self.lyth_bottom_AnalyzePreview.setContentsMargins(-1, -1, 40, -1)
        self.lyth_bottom_AnalyzePreview.setObjectName("lyth_bottom_AnalyzePreview")
        self.btn_back_AnalyzePreview = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_back_AnalyzePreview.sizePolicy().hasHeightForWidth())
        self.btn_back_AnalyzePreview.setSizePolicy(sizePolicy)
        self.btn_back_AnalyzePreview.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_back_AnalyzePreview.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.btn_back_AnalyzePreview.setFont(font)
        self.btn_back_AnalyzePreview.setStatusTip("")
        self.btn_back_AnalyzePreview.setWhatsThis("")
        self.btn_back_AnalyzePreview.setAccessibleName("")
        self.btn_back_AnalyzePreview.setAccessibleDescription("")
        self.btn_back_AnalyzePreview.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")
        self.btn_back_AnalyzePreview.setText("")
        self.btn_back_AnalyzePreview.setIcon(':/icons/back_icon')
        self.btn_back_AnalyzePreview.setIconSize(QtCore.QSize(20, 20))
        self.btn_back_AnalyzePreview.setCheckable(True)
        self.btn_back_AnalyzePreview.setObjectName("btn_back_AnalyzePreview")
        self.lyth_bottom_AnalyzePreview.addWidget(self.btn_back_AnalyzePreview)
        spacerItem50 = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lyth_bottom_AnalyzePreview.addItem(spacerItem50)
        spacerItem51 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bottom_AnalyzePreview.addItem(spacerItem51)
        self.btn_startAnalyze = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_startAnalyze.sizePolicy().hasHeightForWidth())
        self.btn_startAnalyze.setSizePolicy(sizePolicy)
        self.btn_startAnalyze.setMinimumSize(QtCore.QSize(220, 40))
        self.btn_startAnalyze.setMaximumSize(QtCore.QSize(220, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.btn_startAnalyze.setFont(font)
        self.btn_startAnalyze.setStatusTip("")
        self.btn_startAnalyze.setWhatsThis("")
        self.btn_startAnalyze.setAccessibleName("")
        self.btn_startAnalyze.setAccessibleDescription("")
        self.btn_startAnalyze.setStyleSheet("QPushButton{\n""    font: 75 18pt \"MS Shell Dlg 2\" ;\n""    background-color: #1C4481;\n""    border-radius: 5px;\n""    color:white\n""}\n""\n""QPushButton:hover{\n""    border: 2px solid rgb(255, 255, 255)\n""}")
        self.btn_startAnalyze.setText("Analyse starten")
        self.btn_startAnalyze.setCheckable(False)
        self.btn_startAnalyze.setFlat(False)
        self.btn_startAnalyze.setObjectName("btn_startAnalyze")
        self.lyth_bottom_AnalyzePreview.addWidget(self.btn_startAnalyze)
        spacerItem52 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bottom_AnalyzePreview.addItem(spacerItem52)
        self.verticalLayout_5.addLayout(self.lyth_bottom_AnalyzePreview)
        self.stackedWidget.addWidget(self)


# Analyze Screen
class ui_analyzePvScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_analyzePvScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui


# Result Screen
class ui_ResultScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_ResultScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui

# Demo Data Screen
class ui_DemoDataScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_DemoDataScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui


# Info Screen
class ui_InfoScreen(QtWidgets.QWidget):
    def __init__(self, LogicInterface, Gui):
        super(ui_InfoScreen, self).__init__()

        self.logic = LogicInterface
        self.gui = Gui