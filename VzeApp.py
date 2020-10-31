import sys
from gui.VzeGui import *


class GuiInterface:

    def doSomething(self):
        return

    def loadFile(self):
        return

class MyLogic(GuiInterface):

    def __init__(self):
        self.m_var = None

    def doSomething(self):
        print("We are doing something")

    def loadFile(self):
        print("loading file method")


class VzeApp(QtWidgets.QApplication):

    mainWidget = None
    mainLogic = None

    def __init__(self, *args, **kwargs):
        super(VzeApp, self).__init__(*args,**kwargs)

        self.mainLogic = MyLogic()

        self.mainWidget = VzeGui(self.mainLogic)
        self.mainWidget.show()


