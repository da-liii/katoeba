import sys
from PyQt4.QtGui import QMainWindow
from PyQt4 import QtSql,QtCore
from ui_mainwindow import *
import connection
import sentence as st

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.data = connection.Data()
        self.model = QtSql.QSqlTableModel()
        self.initializeModel()
        table = self.createView()
        self.ui.goButton.clicked.connect(self.insertById)

    def insertRecord(self, id, sentence, lang):
        record = QtSql.QSqlRecord();
        f1 = QtSql.QSqlField("id", QtCore.QVariant.Int)
        f2 = QtSql.QSqlField("sentence", QtCore.QVariant.String)
        f3 = QtSql.QSqlField("lang", QtCore.QVariant.String)
        f1.setValue(id)
        f2.setValue(sentence)
        f3.setValue(lang)
        record.append(f1);
        record.append(f2);
        record.append(f3);
        self.model.insertRecord(-1, record)

    def insertById(self):
        id = self.ui.comboBox.currentText().toInt();
        if id[1]:
            sentence = st.getSentenceById(id[0])
        else:
            return
        a,b,c = sentence.split("\t")
        self.insertRecord(a, c, b)



    # involving table view
    def initializeModel(self):
        self.model.setTable('tatoeba')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Sentence")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Language")

    def createView(self):
        view = self.ui.tableView
        view.setModel(self.model)
        return view
