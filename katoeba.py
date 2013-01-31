# -*- coding = utf-8 -*-
import sys
from PyQt4.QtGui import QApplication, QMainWindow
from mainwindow import *

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
