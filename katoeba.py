# -*- coding = utf-8 -*-
import sys
import codecs

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import sentence as st

class Foo(QObject):
    @pyqtSlot(int, result=str)
    def sentenceById(self, value):
        return st.getSentenceById(value)

    @pyqtSlot(int, result=str)
    def translationById(self, value):
        return st.getTranslationById(value)

    @pyqtSlot(str, result=str)
    def sentencesByRegex(self, value):
        return st.getSentencesByRegex(value)

    @pyqtSlot()
    def quit(self):
        QApplication.quit()

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        view = QWebView(self)
        setting = view.page().settings()
        setting.setDefaultTextEncoding("UTF-8")
        layout = QVBoxLayout(self)
        layout.addWidget(view)

        self.foo = Foo(self)
        view.page().mainFrame().addToJavaScriptWindowObject("foo", self.foo)
        html = codecs.open('index.html','r', 'utf-8').read()
        view.setHtml(html)

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
