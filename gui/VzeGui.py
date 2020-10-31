import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class VzeGui(QtWidgets.QMainWindow):

    def __init__(self, logicInterface):
        QtWidgets.QMainWindow.__init__(self)
        print ("loadgig UI")
       
        self.logic = logicInterface
        # Setting Window Title and Icon
        self.setWindowTitle("VerkehrsZeichenErkennung VZE")
        self.setWindowIcon(QtGui.QIcon("gui/pics/Logo_Schild_v1_2020-08-10_TB.png"))
       
       # Size of window is always half size of availabe window
        size = QtWidgets.QDesktopWidget().availableGeometry()
        self.setMinimumSize( size.width() * 0.65, size.height() * 0.65)

        # Main widget
        window = QtWidgets.QWidget()
        window.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.setCentralWidget(window)
        window.setObjectName("window")
        
        # Set vertical layout for main window
        self.verticalLayout = QtWidgets.QVBoxLayout(window)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Set stacked widget
        self.stackedWidget = QtWidgets.QStackedWidget(window)
        self.stackedWidget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.stackedWidget.setObjectName("stackedWidget")
        
        #Build UI
        self.ui_startscreen()
        self.ui_demoscreen()
        self.ui_button_handler(self.logic)

        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(window)

    # Start Screen
    def ui_startscreen(self):
        self.StartScreen = QtWidgets.QWidget()
        self.StartScreen.setStatusTip("")
        self.StartScreen.setWhatsThis("")
        self.StartScreen.setAccessibleName("")
        self.StartScreen.setAccessibleDescription("")
        self.StartScreen.setObjectName("StartScreen")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.StartScreen)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
    
        self.lyth_headline = QtWidgets.QHBoxLayout()
        self.lyth_headline.setContentsMargins(20, -1, 20, 0)
        self.lyth_headline.setObjectName("lyth_headline")
        
        self.lbl_willkommen = QtWidgets.QLabel(self.StartScreen)
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
        self.btn_info_startscreen = QtWidgets.QPushButton(self.StartScreen)
        self.btn_info_startscreen.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_startscreen.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_startscreen.setStatusTip("")
        self.btn_info_startscreen.setWhatsThis("")
        self.btn_info_startscreen.setAccessibleName("")
        self.btn_info_startscreen.setAccessibleDescription("")
        self.btn_info_startscreen.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")
        self.btn_info_startscreen.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui/pics/info_logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.btn_loadFile = QtWidgets.QPushButton(self.StartScreen)
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
        self.btn_loadFile.setStyleSheet("QPushButton{\n""    font: 75 26pt \"MS Shell Dlg 2\" ;\n""    background-color: #1C4481;\n""    border-radius: 5px;\n""    color:white\n""}\n""\n""QPushButton:hover{\n""    border: 2px solid rgb(255, 255, 255)\n""}")
        self.btn_loadFile.setCheckable(False)
        self.btn_loadFile.setFlat(False)
        self.btn_loadFile.setObjectName("btn_loadFile")
        self.lyth_bigBtn.addWidget(self.btn_loadFile)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lyth_bigBtn.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bigBtn.addItem(spacerItem5)
        self.btn_demoToDemo = QtWidgets.QPushButton(self.StartScreen)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_demoToDemo.sizePolicy().hasHeightForWidth())
        
        self.btn_demoToDemo.setSizePolicy(sizePolicy)
        self.btn_demoToDemo.setMinimumSize(QtCore.QSize(350, 220))
        self.btn_demoToDemo.setStyleSheet("QPushButton{\n""    font: 75 26pt \"MS Shell Dlg 2\" ;\n""    background-color: #1C4481;\n""    border-radius: 5px;\n""    color:white\n""}\n""\n""QPushButton:hover{\n""    border: 2px solid rgb(255, 255, 255)\n""}")
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
        self.stackedWidget.addWidget(self.StartScreen)

        self.lbl_willkommen.setText(("Willkommen"))
        self.btn_info_startscreen.setText((""))
        self.btn_loadFile.setText(("Datei auswählen"))
        self.btn_demoToDemo.setText(("Demo auswählen"))

    # Demo Screen
    def ui_demoscreen(self):
        self.DemoScreen = QtWidgets.QWidget()
        self.DemoScreen.setObjectName("DemoScreen")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.DemoScreen)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lyth_headline_demoscreen = QtWidgets.QHBoxLayout()
        self.lyth_headline_demoscreen.setContentsMargins(20, 0, 20, 0)
        self.lyth_headline_demoscreen.setSpacing(6)
        self.lyth_headline_demoscreen.setObjectName("lyth_headline_demoscreen")
        self.lbl_demo = QtWidgets.QLabel(self.DemoScreen)
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
        self.btn_info_demoscreen = QtWidgets.QPushButton(self.DemoScreen)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_info_demoscreen.sizePolicy().hasHeightForWidth())
        self.btn_info_demoscreen.setSizePolicy(sizePolicy)
        self.btn_info_demoscreen.setMinimumSize(QtCore.QSize(140, 45))
        self.btn_info_demoscreen.setMaximumSize(QtCore.QSize(140, 45))
        self.btn_info_demoscreen.setStatusTip("")
        self.btn_info_demoscreen.setWhatsThis("")
        self.btn_info_demoscreen.setAccessibleName("")
        self.btn_info_demoscreen.setAccessibleDescription("")
        self.btn_info_demoscreen.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")
        self.btn_info_demoscreen.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui/pics/info_logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info_demoscreen.setIcon(icon)
        self.btn_info_demoscreen.setIconSize(QtCore.QSize(130, 30))
        self.btn_info_demoscreen.setObjectName("btn_info_demoscreen")
        self.lyth_headline_demoscreen.addWidget(self.btn_info_demoscreen)
        self.verticalLayout_3.addLayout(self.lyth_headline_demoscreen)
        
        
        
        self.lytv_bigCenter_demoScreen = QtWidgets.QVBoxLayout()
        self.lytv_bigCenter_demoScreen.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lytv_bigCenter_demoScreen.setContentsMargins(0, -1, 0, -1)
        self.lytv_bigCenter_demoScreen.setObjectName("lytv_bigCenter_demoScreen")
        self.lyth_smallText_Demo = QtWidgets.QHBoxLayout()
        self.lyth_smallText_Demo.setContentsMargins(20, 0, -1, -1)
        self.lyth_smallText_Demo.setObjectName("lyth_smallText_Demo")
        self.label_demotext = QtWidgets.QLabel(self.DemoScreen)
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
        self.label_demotext.setStatusTip("")
        self.label_demotext.setWhatsThis("")
        self.label_demotext.setAccessibleName("")
        self.label_demotext.setAccessibleDescription("")
        self.label_demotext.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_demotext.setObjectName("label_demotext")
        self.lyth_smallText_Demo.addWidget(self.label_demotext, 0, QtCore.Qt.AlignTop)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_smallText_Demo.addItem(spacerItem11)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lyth_smallText_Demo.addItem(spacerItem12)
        self.lytv_bigCenter_demoScreen.addLayout(self.lyth_smallText_Demo)
        self.lyth_bigBtn_Demo = QtWidgets.QHBoxLayout()
        self.lyth_bigBtn_Demo.setObjectName("lyth_bigBtn_Demo")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bigBtn_Demo.addItem(spacerItem13)
        self.btn_demoSonne = QtWidgets.QPushButton(self.DemoScreen)
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
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lyth_bigBtn_Demo.addItem(spacerItem14)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bigBtn_Demo.addItem(spacerItem15)
        self.btn_demoRegen = QtWidgets.QPushButton(self.DemoScreen)
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
        icon1.addPixmap(QtGui.QPixmap("gui/pics/data-icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.btn_dataSonne = QtWidgets.QPushButton(self.DemoScreen)
        self.btn_dataSonne.setMinimumSize(QtCore.QSize(55, 55))
        self.btn_dataSonne.setMaximumSize(QtCore.QSize(55, 55))
        self.btn_dataSonne.setStyleSheet("QPushButton:hover{\n""    border-radius:5px;\n""    border: 2px solid rgb(255, 255, 255)\n""\n""}")

        self.btn_dataSonne.setIcon(icon1)
        self.btn_dataSonne.setIconSize(QtCore.QSize(55, 55))
        self.btn_dataSonne.setObjectName("btn_dataSonne")
        self.lyth_smallBtn_demoscreen.addWidget(self.btn_dataSonne)

        spacerItem18 = QtWidgets.QSpacerItem(370, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.lyth_smallBtn_demoscreen.addItem(spacerItem18)
        
        self.btn_dataRegen = QtWidgets.QPushButton(self.DemoScreen)
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
        self.btn_back_demoscreen = QtWidgets.QPushButton(self.DemoScreen)
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
        icon2.addPixmap(QtGui.QPixmap("gui/pics/back_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_back_demoscreen.setIcon(icon2)
        self.btn_back_demoscreen.setIconSize(QtCore.QSize(20, 20))
        self.btn_back_demoscreen.setObjectName("btn_back_demoscreen")
        self.lyth_bottom_demoscreen.addWidget(self.btn_back_demoscreen)


        spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lyth_bottom_demoscreen.addItem(spacerItem22)
        spacerItem23 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lyth_bottom_demoscreen.addItem(spacerItem23)
        self.verticalLayout_3.addLayout(self.lyth_bottom_demoscreen)

        self.stackedWidget.addWidget(self.DemoScreen)
        self.verticalLayout.addWidget(self.stackedWidget)
    

        


        self.lbl_demo.setText(("Demo"))
        self.btn_info_demoscreen.setText((""))
        self.label_demotext.setText(("Wählen Sie ein Demovideo aus"))
        self.btn_demoSonne.setText(("Video mit Sonne"))
        self.btn_demoRegen.setText(("Video mit Regen"))
        self.btn_dataSonne.setText((""))
        self.btn_dataRegen.setText((""))
        self.btn_back_demoscreen.setText((""))

        
       
        


        ###################
        ##### Styles ######
        ###################
        styleButton= "QPushButton{\n""    font: 75 26pt \"MS Shell Dlg 2\" ;\n""    background-color: #1C4481;\n""    border-radius: 20px;\n""    color:white\n""}\n""\n""QPushButton:hover{\n""    border: 2px solid rgb(255, 255, 255)\n""}"

    # Button handler with interface
    def ui_button_handler(self, logicInterface):
        self.btn_loadFile.setToolTip('Laden eines Videos oder Bildes')
        self.btn_loadFile.clicked.connect(lambda:logicInterface.loadFile())
        
        
        self.btn_demoToDemo.setToolTip('Demo Videos wählen')
        self.btn_demoToDemo.clicked.connect(lambda:logicInterface.doSomething())
        self.btn_demoToDemo.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))


        self.btn_back_demoscreen.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))


        #self.btn_file.clicked.connect(lambda:logicInterface.loadFile(self.text.text()))
        
      


    