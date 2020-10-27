import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class VzeGui(QMainWindow):

    def __init__(self, logicInteface):
        QMainWindow.__init__(self)
        print ("loadgig widget")
        self.logic = logicInteface

        # Setting Window Title
        self.setWindowTitle("VerkehrsZeichenErkennung VZE")
        self.setWindowIcon(QIcon("gui/pics/Logo_Schild_v1_2020-08-10_TB.png"))
        #self.layout = QVBoxLayout()
        helpWidget = QWidget()
        
        #helpWidget.setLayout(self.layout)
        self.setCentralWidget(helpWidget)
        
        size = QDesktopWidget().availableGeometry()
        self.setFixedSize( size.width() * 0.5, size.height() * 0.5)

        # UI Elements
       
        self.btn_file = QPushButton("Datei wählen")
        self.btn_file.resize(300,300)
        self.btn_file.setToolTip('Laden eines Videos oder Bildes')
        self.btn_file.setCheckable(True)
        self.btn_file.clicked.connect(lambda:logicInteface.doSomething())
        #self.btn_file.clicked.connect(lambda:logicInteface.loadFile(self.text.text()))
        #self.layout.addWidget(self.btn_file)
      


    