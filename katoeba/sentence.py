# -*- coding:utf-8 -*-
from PyQt4 import QtCore, QtSql
from subprocess import check_output

parser = "tatoparser"
show_id = "--display-ids"
show_lang = "--display-lang"

class Sentence(QtCore.QThread):
    sendMessage = QtCore.pyqtSignal(str)
    insertModel = QtCore.pyqtSignal(dict)
    def __init__(self, ddict, parent):
        super(Sentence, self).__init__()
        self.dict = ddict
        self.sendMessage.connect(parent.showMessage)
        self.insertModel.connect(parent.insertSentence)

    def run(self):
        self.insertSentence()

    def insertSentence(self):
        prog = [parser, show_id, show_lang]
        for key in self.dict.keys():
            if self.dict[key] != "all" and key != "ui":
                prog.append(key)
                prog.append(self.dict[key])
        print prog
        self.sendMessage.emit(" ".join(prog))
        isTr = 'r'
        if '--is-linked-to' in self.dict.keys():
            isTr = 't'
        elif '-t' in self.dict.keys():
            isTr = 't'
        sentences = unicode(
            check_output(prog),
            'utf-8').rstrip("\n")
        self.dict["isTr"] = isTr
        self.dict["st"] = sentences
        self.insertModel.emit(self.dict)
