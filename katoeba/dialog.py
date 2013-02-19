from ui_list import *
from PyQt4 import QtGui

class Dialog(QtGui.QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

